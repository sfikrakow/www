from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from common.models import NavigationMenuEntry


@register(NavigationMenuEntry)
class PostTR(TranslationOptions):
    fields = ('link_title',)
