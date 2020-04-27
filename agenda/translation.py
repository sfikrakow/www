from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from agenda.models import SpeakerIndex, Speaker


@register(Speaker)
class SpeakerTR(TranslationOptions):
    fields = ('content',)


@register(SpeakerIndex)
class SpeakerIndexTR(TranslationOptions):
    pass
