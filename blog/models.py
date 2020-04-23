from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from common.models import SFIPage


class PostIndex(SFIPage):
    subpage_types = ['Post']

    POSTS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = Post.objects.live().public().order_by('-date')
        paginator = Paginator(all_posts, PostIndex.POSTS_PER_PAGE)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
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
