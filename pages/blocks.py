from wagtail.core.blocks import StructBlock, PageChooserBlock, IntegerBlock, RichTextBlock, TextBlock


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
