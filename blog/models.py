from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from common.models import SFIPage
from common.utils import paginate

DEFAULT_PAGINATION = 20  # the number should be even (two column view).


class PostIndex(SFIPage):
    subpage_types = ['Post']

    POSTS_PER_PAGE = DEFAULT_PAGINATION

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = paginate(
            Post.objects.live().public().descendant_of(self).order_by('-date'),
            request, PostIndex.POSTS_PER_PAGE)
        return context

    class Meta:
        verbose_name = _('post index')
        verbose_name_plural = _('post indexes')


class Post(SFIPage):
    content = RichTextField(verbose_name=_('content'))

    date = models.DateTimeField(default=timezone.now, verbose_name=_('post date'))

    redirect_to = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_('redirect to page'),
        help_text=_(
            'Redirect to a specified page instead of showing content. '
            'You should still add content or description to show in previews.')
    )

    content_panels = SFIPage.content_panels + [
        FieldPanel('date'),
        FieldPanel('content'),
    ]

    settings_panels = SFIPage.settings_panels + [
        PageChooserPanel('redirect_to'),
    ]

    parent_page_types = ['PostIndex']
    subpage_types = []

    def serve(self, request, *args, **kwargs):
        if self.redirect_to:
            return redirect(self.redirect_to.url)
        return super().serve(request, *args, **kwargs)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
