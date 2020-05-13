from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from agenda.models import SpeakerIndex, Speaker, Edition, EditionIndex, CategoryIndex, Category, EventIndex, Event


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
    pass


@register(CategoryIndex)
class CategoryIndexTR(TranslationOptions):
    pass


@register(Category)
class CategoryTR(TranslationOptions):
    pass


@register(EventIndex)
class EventIndexTR(TranslationOptions):
    pass


@register(Event)
class EventTR(TranslationOptions):
    fields = ('content',)