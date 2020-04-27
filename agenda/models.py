from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from common.models import SFIPage


class SpeakerIndex(SFIPage):
    subpage_types = ['Speaker']

    SPEAKERS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = Speaker.objects.live().public()
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

    content_panels = SFIPage.content_panels + [
        FieldPanel('content')
    ]

    parent_page_types = ['SpeakerIndex']
    subpage_types = []
