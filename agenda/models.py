from enum import Enum

from django.core.validators import RegexValidator
from django.db import models
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.embeds.models import Embed
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from common.models import SFIPage
from common.utils import paginate


@register_snippet
class Sponsor(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"


class SpeakerIndex(SFIPage):
    subpage_types = ['Speaker']

    SPEAKERS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['speakers'] = paginate(
            Speaker.objects.live().public().descendant_of(self).order_by('title'),
            request, SpeakerIndex.SPEAKERS_PER_PAGE)
        return context

    class Meta:
        verbose_name = 'Speakers index'
        verbose_name_plural = 'Speakers indexes'


class Speaker(SFIPage):
    content = RichTextField()
    sponsor = models.ForeignKey(Sponsor, null=True, blank=True, on_delete=models.PROTECT)

    content_panels = SFIPage.content_panels + [
        FieldPanel('content'),
        SnippetChooserPanel('sponsor'),
        InlinePanel('social_links', label='Social links')
    ]

    parent_page_types = ['SpeakerIndex']
    subpage_types = []

    class Meta:
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'


class SocialLinkTypes(models.TextChoices):
    FACEBOOK = 'facebook', 'Facebook'
    TWITTER = 'twitter', 'Twitter'
    GITHUB = 'github', 'Github'
    INSTAGRAM = 'instagram', 'Instagram'
    LINKEDIN = 'linkedin', 'Linkedin'
    EMAIL = 'email', _('Email')
    WEBSITE = 'site', _('Website')
    OTHER = 'other', _('Other')


class SocialLink(models.Model):
    speaker = ParentalKey(Speaker, on_delete=models.CASCADE, related_name='social_links')
    type = models.CharField(max_length=16, choices=SocialLinkTypes.choices, default=SocialLinkTypes.OTHER)
    link = models.URLField(max_length=512)


class EditionIndex(SFIPage):
    subpage_types = ['Edition']

    EDITIONS_PER_PAGE = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['editions'] = Edition.objects.live().public().descendant_of(self)
        return context

    class Meta:
        verbose_name = 'Edition index'
        verbose_name_plural = 'Edition indexes'


class Edition(SFIPage):
    start_date = models.DateTimeField("Edition start date", null=True, blank=True)
    end_date = models.DateTimeField("Edition end date", null=True, blank=True)

    content_panels = SFIPage.content_panels + [
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        InlinePanel('event_categories', label='Event categories')
    ]

    parent_page_types = ['EditionIndex']
    subpage_types = ['EventIndex']

    class Meta:
        verbose_name = 'Edition'
        verbose_name_plural = 'Editions'


class Category(models.Model):
    edition = ParentalKey(Edition, on_delete=models.CASCADE, related_name='event_categories')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=300)
    color = models.CharField("Category color",
                             max_length=7,
                             default='#23211f',
                             validators=[RegexValidator(
                                 regex=r'^#([0-9a-fA-F]{6})$',
                                 message=_('Color must be in hex'),
                             ), ])

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('color', widget=TextInput(attrs={'type': 'color', 'style': 'height:60'}))
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event category'
        verbose_name_plural = 'Event categories'


class EventIndex(SFIPage):
    parent_page_types = ['Edition']
    subpage_types = ['Event']

    color = models.CharField("Index color",
                             max_length=7,
                             default='#23211f',
                             validators=[RegexValidator(
                                 regex=r'^#([0-9a-fA-F]{6})$',
                                 message=_('Color must be in hex'),
                             ), ])

    content_panels = SFIPage.content_panels + [
        FieldPanel('color', widget=TextInput(attrs={'type': 'color', 'style': 'height:60'}))
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # TODO: display agenda block??
        return context

    class Meta:
        verbose_name = 'Event list'
        verbose_name_plural = 'Event lists'


class LanguageChoice(models.TextChoices):
    POLISH = 'pl', _('Polish')
    ENGLISH = 'en', _('English')


class Event(SFIPage):
    content = RichTextField()
    date = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    event_speaker = models.ForeignKey(Speaker, null=True, on_delete=models.PROTECT)
    event_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    language = models.CharField(max_length=5, choices=LanguageChoice.choices, null=True, blank=True)
    sponsor = models.ForeignKey(Sponsor, null=True, blank=True, on_delete=models.PROTECT)
    recording = models.URLField(max_length=512, null=True, blank=True)

    class EventCategoryFieldPanel(FieldPanel):
        # Terrible hack to limit category choices to edition.
        def on_form_bound(self):
            edition_page = self.form.parent_page.get_parent().edition
            choices = edition_page.event_categories.all()
            self.form.fields['event_category'].queryset = choices
            super().on_form_bound()

    content_panels = SFIPage.content_panels + [
        FieldPanel('content'),
        FieldPanel('date'),
        FieldPanel('duration_minutes'),
        PageChooserPanel('event_speaker'),
        EventCategoryFieldPanel('event_category'),
        FieldPanel('language'),
        SnippetChooserPanel('sponsor'),
        FieldPanel('recording')
    ]

    parent_page_types = ['EventIndex']
    subpage_types = []

    @property
    def index(self):
        return self.get_parent()

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
