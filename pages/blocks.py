import random

from wagtail.core.blocks import StructBlock, RichTextBlock, TextBlock


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

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['block_id'] = random.randint(0, 100000000)
        return context

    class Meta:
        template = 'pages/dropdown_block.html'
