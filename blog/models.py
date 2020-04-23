from datetime import datetime

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from common.models import SFIPage


class PostIndex(SFIPage):
    subpage_types = ['Post']


class Post(SFIPage):
    content = RichTextField()

    date = models.DateTimeField("Post date", default=datetime.now)

    content_panels = SFIPage.content_panels + [
        FieldPanel('date'),
        FieldPanel('content'),
    ]

    parent_page_types = ['PostIndex']
    subpage_types = []
