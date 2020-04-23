from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from blog.models import Post, PostIndex


@register(Post)
class PostTR(TranslationOptions):
    fields = ('content',)


@register(PostIndex)
class PostIndexTR(TranslationOptions):
    pass
