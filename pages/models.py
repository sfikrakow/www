from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core import blocks
from wagtail.core.blocks import RawHTMLBlock
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from agenda.blocks import EventIndexBlock
from blog.blocks import PostIndexBlock
from common.cache import InvalidateCacheMixin
from common.models import SFIPage
from pages.blocks import HeadingBlock, SectionTitleBlock, SectionDividerBlock, DropdownBlock, PhotoGallery, MapBlock, \
    SectionSubtitleBlock


class StaticPage(SFIPage):
    content = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('post_index', PostIndexBlock()),
        ('event_index', EventIndexBlock()),
        ('header', HeadingBlock()),
        ('section_title', SectionTitleBlock()),
        ('section_subtitle', SectionSubtitleBlock()),
        ('section_divider', SectionDividerBlock()),
        ('dropdown', DropdownBlock()),
        ('photo_gallery', PhotoGallery()),
        ('map', MapBlock()),
        ('raw_html', RawHTMLBlock()),
    ], null=True, blank=True, verbose_name=_('content'))

    content_panels = SFIPage.content_panels + [
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')


@register_setting(icon='view')
class FooterSettings(BaseSetting, InvalidateCacheMixin):
    content = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('header', HeadingBlock()),
        ('section_title', SectionTitleBlock()),
        ('section_subtitle', SectionSubtitleBlock()),
        ('section_divider', SectionDividerBlock()),
        ('dropdown', DropdownBlock()),
        ('photo_gallery', PhotoGallery()),
        ('raw_html', RawHTMLBlock()),
    ], null=True, blank=True, verbose_name=_('content'))

    panels = [
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = _('footer settings')
