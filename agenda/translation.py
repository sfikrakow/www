from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from agenda.models import SpeakerIndex, Speaker, Edition, EditionIndex, EventIndex, Event, Category


@register(SpeakerIndex)
class SpeakerIndexTR(TranslationOptions):
    pass


@register(Speaker)
class SpeakerTR(TranslationOptions):
    fields = ('content',)


@register(EditionIndex)
class EditionIndexTR(TranslationOptions):
    pass


@register(Edition)
class EditionTR(TranslationOptions):
    fields = ('edition_footer',)


@register(Category)
class CategoryTR(TranslationOptions):
    fields = ('name',)


@register(EventIndex)
class EventIndexTR(TranslationOptions):
    pass


@register(Event)
class EventTR(TranslationOptions):
    fields = ('content',)
