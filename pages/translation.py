from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from pages.models import StaticPage


@register(StaticPage)
class StaticPageTR(TranslationOptions):
    fields = ('content',)
