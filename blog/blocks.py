from wagtail.core.blocks import StructBlock, PageChooserBlock, IntegerBlock

from blog.models import Post


class PostIndexBlock(StructBlock):
    index = PageChooserBlock(page_type=['blog.PostIndex'])
    shown_posts = IntegerBlock(min_value=1)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['posts'] = Post.objects.live().public() \
            .descendant_of(value['index']).order_by('-date')[
            :value['shown_posts']]
        return context

    class Meta:
        template = 'blog/post_index_block.html'
        icon = 'index'
