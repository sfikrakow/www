from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from pages.models import StaticPage, FooterSettings


@register(StaticPage)
class StaticPageTR(TranslationOptions):
    fields = ('content',)


@register(FooterSettings)
class FooterSettingsTR(TranslationOptions):
    fields = ('content',)
