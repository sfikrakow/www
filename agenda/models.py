from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from wagtail.images.edit_handlers import ImageChooserPanel

from common.models import SFIPage


class SpeakerIndex(SFIPage):
    subpage_types = ['Speaker']

    SPEAKERS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = Speaker.objects.live().public().order_by('last_name')
        paginator = Paginator(all_posts, SpeakerIndex.SPEAKERS_PER_PAGE)
        page = request.GET.get('page')
        try:
            speakers = paginator.page(page)
        except PageNotAnInteger:
            speakers = paginator.page(1)
        except EmptyPage:
            speakers = paginator.page(paginator.num_pages)
        context['speakers'] = speakers
        return context


class Speaker(SFIPage):
    content = RichTextField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    content_panels = SFIPage.content_panels + [
        FieldPanel('content')
    ]

    parent_page_types = ['SpeakerIndex']
    subpage_types = []


class EditionIndex(SFIPage):
    subpage_types = ['Edition']

    EDITIONS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = Edition.objects.live().public().order_by('-date')
        paginator = Paginator(all_posts, EditionIndex.EDITIONS_PER_PAGE)
        page = request.GET.get('page')
        try:
            editions = paginator.page(page)
        except PageNotAnInteger:
            editions = paginator.page(1)
        except EmptyPage:
            editions = paginator.page(paginator.num_pages)
        context['editions'] = editions
        return context


class Edition(SFIPage):
    number = models.IntegerField("Edition number")
    start_date = models.DateTimeField("Edition date", default=datetime.now)

    content_panels = SFIPage.content_panels + [
        FieldPanel('number'),
        FieldPanel('start_date')
    ]

    parent_page_types = ['EditionIndex']
    subpage_types = ['CategoryIndex', 'EventIndex']


class CategoryIndex(SFIPage):
    subpage_types = ['Category']
    parent_page_types = ['Edition']

    CATEGORIES_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = Category.objects.live().public().order_by('name')
        paginator = Paginator(all_posts, CategoryIndex.CATEGORIES_PER_PAGE)
        page = request.GET.get('page')
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)
        context['categories'] = categories
        return context


class Category(SFIPage):
    name = models.CharField(max_length=300)
    icon = models.CharField(max_length=300)
    color = models.CharField("Category color",
                             max_length=7,
                             default='#23211f',
                             validators=[RegexValidator(
                                 regex=r'^#([0-9a-fA-F]{6})$',
                                 message=_('Username must be Alphanumeric'),
                             ),
                             ])

    content_panels = SFIPage.content_panels + [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('color')
    ]

    parent_page_types = ['CategoryIndex']
    subpage_types = []


class EventIndex(SFIPage):
    parent_page_types = ['Edition']
    subpage_types = ['Event']

    EVENTS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = Event.objects.live().public().order_by('-date')
        paginator = Paginator(all_posts, EventIndex.EVENTS_PER_PAGE)
        page = request.GET.get('page')
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)
        context['events'] = events
        return context


class Event(SFIPage):
    content = RichTextField()
    date = models.DateTimeField()
    event_speaker = models.ForeignKey(Speaker, null=True, on_delete=models.SET_NULL)
    event_category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    content_panels = SFIPage.content_panels + [
        FieldPanel('content'),
        FieldPanel('date'),
        FieldPanel('event_speaker'),
        FieldPanel('event_category')
    ]

    parent_page_types = ['EventIndex']
    subpage_types = []
