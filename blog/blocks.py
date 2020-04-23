from wagtail.core.blocks import StructBlock, PageChooserBlock, IntegerBlock


class PostIndexBlock(StructBlock):
    index = PageChooserBlock(page_type=['PostIndex'])
    shown_posts = IntegerBlock(min_value=1)

    class Meta:
        template = 'blog/post_index_block.html'
