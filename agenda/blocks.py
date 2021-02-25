from wagtail.core.blocks import StructBlock, PageChooserBlock, IntegerBlock

import agenda.models


class AgendaBlock(StructBlock):
    index = PageChooserBlock(page_type=['EditionIndex'])

    class Meta:
        template = 'agenda/agenda_block.html'


class EventIndexBlock(StructBlock):
    index = PageChooserBlock(page_type=['agenda.EventIndex'])
    shown_posts = IntegerBlock(min_value=1)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['posts'] = agenda.models.Event.objects.live().public().descendant_of(value['index']).order_by('-date')[
                           :value['shown_posts']]
        return context

    class Meta:
        template = 'agenda/event_index_block.html'
        icon = 'index'
