from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from home.models import HomePage


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = ('content',)
