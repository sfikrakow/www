import random

from wagtail.core.blocks import StructBlock, RichTextBlock, TextBlock, ListBlock, URLBlock, IntegerBlock, BooleanBlock, \
    FloatBlock, PageChooserBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock


class MenuItem(StructBlock):
    name = CharBlock(max_length=100)
    link_page = PageChooserBlock(required=False)
    link_url = URLBlock(required=False)


class HeadingBlock(StructBlock):
    content = RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'link', 'document-link'])
    buttons = ListBlock(MenuItem(), required=False, default=[])

    class Meta:
        template = 'common/blocks/heading_block.html'


class SectionTitleBlock(StructBlock):
    title = TextBlock()

    class Meta:
        template = 'common/blocks/section_title_block.html'


class SectionSubtitleBlock(StructBlock):
    title = TextBlock()

    class Meta:
        template = 'common/blocks/section_subtitle_block.html'


class SectionDividerBlock(StructBlock):
    title = TextBlock()

    class Meta:
        template = 'common/blocks/section_divider_block.html'


class DropdownBlock(StructBlock):
    title = TextBlock()
    content = RichTextBlock()

    class Meta:
        template = 'common/blocks/dropdown_block.html'


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
        photo_sizes = [(p['photo'].width, p['photo'].height) for p in value['photos']]
        if value['crop_to_fit']:
            context['max_height'] = int(min(value['image_height'], max((p[1] for p in photo_sizes))))
        else:
            context['max_height'] = int(min(value['image_height'],
                                            max((min(h, value['image_width'] * (h / w)) for w, h in photo_sizes))))
        return context

    class Meta:
        template = 'common/blocks/photo_gallery_block.html'


class MapMarker(StructBlock):
    name = TextBlock()
    longitude = FloatBlock()
    latitude = FloatBlock()


class MapBlock(StructBlock):
    center_longitude = FloatBlock()
    center_latitude = FloatBlock()
    zoom = FloatBlock()
    bearing = FloatBlock()
    pitch = FloatBlock()
    markers = ListBlock(MapMarker)
    placeholder = ImageChooserBlock(help_text="Insert a screenshot of the map here")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['random_id'] = random.randint(1, 1000000000)
        return context

    class Meta:
        template = 'common/blocks/map_block.html'
