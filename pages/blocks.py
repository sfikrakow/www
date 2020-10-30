import random

from wagtail.core.blocks import StructBlock, RichTextBlock, TextBlock, ListBlock, URLBlock, IntegerBlock, BooleanBlock
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(StructBlock):
    content = RichTextBlock()

    class Meta:
        template = 'pages/heading_block.html'


class SectionTitleBlock(StructBlock):
    title = TextBlock()

    class Meta:
        template = 'pages/section_title_block.html'


class SectionDividerBlock(StructBlock):
    title = TextBlock()

    class Meta:
        template = 'pages/section_divider_block.html'


class DropdownBlock(StructBlock):
    title = TextBlock()
    content = RichTextBlock()

    class Meta:
        template = 'pages/dropdown_block.html'


class PhotoGalleryItem(StructBlock):
    title = TextBlock(required=False)
    photo = ImageChooserBlock()
    link = URLBlock(required=False)


class PhotoGallery(StructBlock):
    image_height = IntegerBlock(min_value=0, max_value=2000, default=200)
    image_width = IntegerBlock(min_value=0, max_value=2000, default=200)
    crop_to_fit = BooleanBlock(default=False, required=False)
    photos = ListBlock(PhotoGalleryItem())

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['image_format'] = "{}-{}x{}".format(
            'fill' if value['crop_to_fit'] else 'max',
            value['image_width'],
            value['image_height'])
        return context

    class Meta:
        template = 'pages/photo_gallery_block.html'
