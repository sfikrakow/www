from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from blog.blocks import PostIndexBlock
from common.models import SFIPage
from pages.blocks import HeadingBlock, SectionTitleBlock, SectionDividerBlock, DropdownBlock, PhotoGallery


class StaticPage(SFIPage):
    content = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('post_index', PostIndexBlock()),
        ('header', HeadingBlock()),
        ('section_title', SectionTitleBlock()),
        ('section_divider', SectionDividerBlock()),
        ('dropdown', DropdownBlock()),
        ('photo_gallery', PhotoGallery())
    ], null=True, blank=True, verbose_name=_('content'))

    content_panels = SFIPage.content_panels + [
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')


@register_setting(icon='view')
class FooterSettings(BaseSetting):
    content = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('header', HeadingBlock()),
        ('section_title', SectionTitleBlock()),
        ('section_divider', SectionDividerBlock()),
        ('dropdown', DropdownBlock()),
        ('photo_gallery', PhotoGallery())
    ], null=True, blank=True, verbose_name=_('content'))

    panels = [
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = _('footer settings')
