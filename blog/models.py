from datetime import datetime

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from common.models import SFIPage
from common.utils import paginate


class PostIndex(SFIPage):
    subpage_types = ['Post']

    POSTS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = paginate(
            Post.objects.live().public().descendant_of(self).order_by('-date'),
            request, PostIndex.POSTS_PER_PAGE)
        return context


class Post(SFIPage):
    content = RichTextField()

    date = models.DateTimeField("Post date", default=datetime.now)

    content_panels = SFIPage.content_panels + [
        FieldPanel('date'),
        FieldPanel('content'),
    ]

    parent_page_types = ['PostIndex']
    subpage_types = []
