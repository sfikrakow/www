import datetime
from collections import defaultdict, deque
from dataclasses import dataclass
from operator import itemgetter
from typing import List, Optional, Union, Tuple

from django.utils import timezone
from wagtail.core.blocks import StructBlock, PageChooserBlock, IntegerBlock

import agenda.models


def _time2min(t: datetime.time):
    return t.hour * 60 + t.minute


@dataclass(frozen=True)
class AgendaEntry:
    start_time: datetime.time
    duration_minutes: int

    @property
    def start_time_min(self):
        return _time2min(self.start_time)

    @property
    def end_time_min(self):
        return self.start_time_min + self.duration_minutes

    @property
    def end_time(self):
        m = self.start_time.minute + self.duration_minutes
        h = self.start_time.hour + (m // 60)
        m = m % 60
        if h > 23:
            return datetime.time(hour=23, minute=59, tzinfo=timezone.get_current_timezone())
        else:
            return datetime.time(hour=h, minute=m)


@dataclass(frozen=True)
class AgendaEvent(AgendaEntry):
    title: str
    speakers: str
    url: str
    language: str
    bg_color_hex: str
    group_icon: Optional[str] = None
    group_icon_color_hex: Optional[str] = None
    is_break = False


@dataclass(frozen=True)
class AgendaBreak(AgendaEntry):
    is_break = True


@dataclass(frozen=True)
class AgendaColumn:
    entries: List[Union[AgendaBreak, AgendaEvent]]


@dataclass(frozen=True)
class AgendaRow(AgendaEntry):
    columns: List[AgendaColumn]


@dataclass(frozen=True)
class AgendaDay(AgendaEntry):
    rows: List[AgendaRow]
    date: datetime.date


class AgendaBlock(StructBlock):
    # Assumes that all events begin and end on the same day (local time).
    index = PageChooserBlock(page_type=['agenda.EventIndex', 'agenda.Edition'])

    @staticmethod
    def _create_event_stream(events: List[AgendaEvent], stream_start_time: datetime.time
                             ) -> Tuple[datetime.time, int, List[AgendaRow]]:
        @dataclass(frozen=True, init=False)
        class IntervalEvent:
            time: datetime.time
            event: AgendaEvent
            is_end: bool = False

            def __init__(self, time: datetime.time, event, is_end):
                object.__setattr__(self, 'time', datetime.time(hour=time.hour, minute=time.minute, tzinfo=time.tzinfo))
                object.__setattr__(self, 'event', event)
                object.__setattr__(self, 'is_end', is_end)

        # do a first fit on intervals to divide them into columns.
        interval_events = [IntervalEvent(ev.start_time, ev, False) for ev in events] + [
            IntervalEvent(ev.end_time, ev, True) for ev in events]
        interval_events = sorted(interval_events, key=lambda x: x.time)
        first_fit: deque[List[List[AgendaEvent]]] = deque([])
        ev_idx = 0
        open_intervals = 0
        while ev_idx < len(interval_events):
            columns: List[List[AgendaEvent]] = []
            while True:
                ev_interval = interval_events[ev_idx]
                ev = ev_interval.event
                ev_idx += 1
                if ev_interval.is_end:
                    open_intervals -= 1
                else:
                    open_intervals += 1
                    first_fit_col_id = next(
                        (idx for idx, col in enumerate(columns) if col[-1].end_time_min <= ev.start_time_min), -1)
                    if first_fit_col_id >= 0:
                        columns[first_fit_col_id].append(ev)
                    else:
                        columns.append([ev])
                if open_intervals == 0:
                    break
            first_fit.append(columns)
        # merge blocks with the same number of columns.
        merged: List[List[List[AgendaEvent]]] = []
        while len(first_fit) > 0:
            current = first_fit.popleft()
            while len(first_fit) > 0 and len(current) == len(first_fit[0]):
                nxt = first_fit.popleft()
                for i in range(len(current)):
                    current[i] += nxt[i]
            merged.append(current)
        # insert AgendaBreak between events in columns and pad columns to block length.
        processed: List[AgendaRow] = []
        last_block_end = stream_start_time
        for idx, block in enumerate(merged):
            block_start = min(col[0].start_time for col in block)
            block_end = max(col[-1].end_time for col in block)
            row: List[AgendaColumn] = []
            if block_start > last_block_end:
                if len(block) != 1:
                    # more than one column - add padding row.
                    processed.append(AgendaRow(last_block_end, _time2min(block_start) - _time2min(last_block_end), [
                        AgendaColumn([AgendaBreak(last_block_end, _time2min(block_start) - _time2min(last_block_end))])
                    ]))
                    last_block_end = block_start
                else:
                    # single column - apply padding to the column itself.
                    block_start = last_block_end
            for col in block:
                column: List[Union[AgendaBreak, AgendaEvent]] = []
                col_time = block_start
                for ev in col:
                    if ev.start_time > col_time:
                        column.append(AgendaBreak(col_time, ev.start_time_min - _time2min(col_time)))
                    column.append(ev)
                    col_time = ev.end_time
                if col_time < block_end:
                    column.append(AgendaBreak(col_time, _time2min(block_end) - _time2min(col_time)))
                row.append(AgendaColumn(column))
            processed.append(AgendaRow(last_block_end, _time2min(block_end) - _time2min(last_block_end), row))
            last_block_end = block_end
        return processed[0].start_time, sum(r.duration_minutes for r in processed), processed

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        events = list(agenda.models.Event.objects.live().public().exclude(date__isnull=True).exclude(
            duration_minutes__isnull=True).descendant_of(value['index']).all())
        if len(events) == 0:
            context['days'] = []
            return context
        days_set = defaultdict(list)
        for event in events:
            date: datetime.datetime = event.date
            local_datetime = timezone.localtime(date)
            days_set[local_datetime.date()].append(event)
        days_events: List[Tuple[datetime.date, List[AgendaEvent]]] = [(day, sorted([
            AgendaEvent(
                start_time=timezone.localtime(e.date).time(),
                duration_minutes=e.duration_minutes,
                title=e.title,
                speakers=', '.join([s.speaker.title for s in e.event_speakers.all()]),
                url=e.url,
                language=e.language,
                bg_color_hex=e.index().color,
                group_icon=e.event_category.icon if e.event_category else None,
                group_icon_color_hex=e.event_category.color if e.event_category else None,
            ) for e in day_list], key=lambda x: x.start_time))
                                                                      for day, day_list in
                                                                      sorted(days_set.items(), key=itemgetter(0))]

        earliest_start = min(e[1][0].start_time for e in days_events)
        streams: List[Tuple[datetime.date, Tuple[datetime.time, int, List[AgendaRow]]]] = [
            (d, self._create_event_stream(ev, earliest_start)) for d, ev in days_events]
        days: List[AgendaDay] = [AgendaDay(start_time, duration, stream, date)
                                 for date, (start_time, duration, stream) in streams]
        context['agenda'] = days
        return context

    class Meta:
        template = 'agenda/agenda_block.html'


class EventIndexBlock(StructBlock):
    index = PageChooserBlock(page_type=['agenda.EventIndex', 'agenda.Edition'])
    shown_posts = IntegerBlock(min_value=1)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['posts'] = agenda.models.Event.objects.live().public().descendant_of(value['index']).order_by('-date')[
                           :value['shown_posts']]
        return context

    class Meta:
        template = 'agenda/event_index_block.html'
        icon = 'index'


class EventScheduleBlock(StructBlock):
    index = PageChooserBlock(page_type=['agenda.EventIndex', 'agenda.Edition'])

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        events = agenda.models.Event.objects.live().public().exclude(date__isnull=True).descendant_of(
            value['index']).order_by('date')
        days = defaultdict(list)
        for event in events:
            date: datetime.datetime = event.date
            days[(date.year, date.month, date.day)].append(event)
        context['days'] = days.values()
        return context

    class Meta:
        template = 'agenda/schedule_block.html'
        icon = 'index'
