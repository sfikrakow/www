from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from agenda.models import SpeakerIndex, Speaker, Edition, EditionIndex, Categories, Category, Events, Event


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


@register(Categories)
class CategoriesTR(TranslationOptions):
    pass


@register(Category)
class CategoryTR(TranslationOptions):
    fields = ('name',)


@register(Events)
class EventsTR(TranslationOptions):
    pass


@register(Event)
class EventTR(TranslationOptions):
    field = ('content',)
