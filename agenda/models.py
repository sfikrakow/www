from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TextInput

from common.models import SFIPage
from common.utils import paginate


class SpeakerIndex(SFIPage):
    subpage_types = ['Speaker']

    SPEAKERS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['speakers'] = paginate(
            Speaker.objects.live().public().descendant_of(self).order_by('title'),
            request, SpeakerIndex.SPEAKERS_PER_PAGE)
        return context


class Speaker(SFIPage):
    content = RichTextField()

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
        context['editions'] = Edition.objects.live().public().descendant_of(self)
        return context


class Edition(SFIPage):
    start_date = models.DateTimeField("Edition start date", null=True, blank=True)
    end_date = models.DateTimeField("Edition end date", null=True, blank=True)

    content_panels = SFIPage.content_panels + [
        FieldPanel('start_date'),
        FieldPanel('end_date'),
    ]

    parent_page_types = ['EditionIndex']
    subpage_types = ['CategoryIndex', 'EventIndex']


class CategoryIndex(SFIPage):
    subpage_types = ['Category']
    parent_page_types = ['Edition']

    CATEGORIES_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['categories'] = Category.objects.live().public().order_by('title')
        return context


class Category(SFIPage):
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
        FieldPanel('icon'),
        FieldPanel('color', widget=TextInput(attrs={'type': 'color', 'style': 'height:60'}))
    ]

    parent_page_types = ['CategoryIndex']
    subpage_types = []


class EventIndex(SFIPage):
    parent_page_types = ['Edition']
    subpage_types = ['Event']

    EVENTS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # TODO: display agenda block??
        return context


class Event(SFIPage):
    content = RichTextField()
    date = models.DateTimeField(null=True, blank=True)
    event_speaker = models.ForeignKey(Speaker, null=True, on_delete=models.SET_NULL)
    event_category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    content_panels = SFIPage.content_panels + [
        FieldPanel('content'),
        FieldPanel('date'),
        PageChooserPanel('event_speaker'),
        PageChooserPanel('event_category')
    ]

    parent_page_types = ['EventIndex']
    subpage_types = []
