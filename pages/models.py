from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from blog.blocks import PostIndexBlock
from common.models import SFIPage


class StaticPage(SFIPage):
    content = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('post_index', PostIndexBlock()),
    ])

    content_panels = SFIPage.content_panels + [
        StreamFieldPanel('content'),
    ]