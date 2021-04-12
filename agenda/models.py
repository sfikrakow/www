from abc import abstractmethod
from collections import defaultdict

from django.core.validators import RegexValidator
from django.db import models
from django.forms.widgets import TextInput
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.blocks import RawHTMLBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.embeds.models import Embed
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from agenda.blocks import AgendaBlock, EventIndexBlock, EventScheduleBlock
from common.blocks import SectionTitleBlock, SectionSubtitleBlock, SectionDividerBlock, DropdownBlock, PhotoGallery, \
    MapBlock
from common.cache import InvalidateCacheMixin
from common.models import SFIPage, AudioFile, ThemeSettings
from common.utils import paginate, with_context, copy_multi_lang

DEFAULT_PAGINATION = 20  # the number should be even (two column view).


@register_snippet
class Sponsor(InvalidateCacheMixin, models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('logo')
    )
    link = models.URLField(max_length=500, null=True,
                           blank=True, verbose_name=_('link'))

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")


class SpeakerIndex(SFIPage):
    subpage_types = ['Speaker']

    SPEAKERS_PER_PAGE = DEFAULT_PAGINATION

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = paginate(
            Speaker.objects.live().public().descendant_of(self).order_by('title'),
            request, SpeakerIndex.SPEAKERS_PER_PAGE)
        return context

    class Meta:
        verbose_name = _('speakers index')
        verbose_name_plural = _('speakers indexes')


class Speaker(SFIPage):
    content = RichTextField(verbose_name=_('content'))
    sponsor = models.ForeignKey(
        Sponsor, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('sponsor'))

    content_panels = SFIPage.content_panels + [
        FieldPanel('content'),
        SnippetChooserPanel('sponsor'),
        InlinePanel('social_links', label='Social links')
    ]

    parent_page_types = ['SpeakerIndex']
    subpage_types = []

    def get_all_events_by_edition(self):
        by_edition = defaultdict(list)
        for event_speaker in self.event_speakers.all():
            if event_speaker.event.live:
                by_edition[event_speaker.event.get_edition()].append(
                    event_speaker.event)
        return sorted(by_edition.items(), key=lambda x: x[0].start_date if x[0].start_date else timezone.now(),
                      reverse=True)

    class Meta:
        verbose_name = _('speaker')
        verbose_name_plural = _('speakers')


class SocialLinkTypes(models.TextChoices):
    FACEBOOK = 'facebook', 'Facebook'
    TWITTER = 'twitter', 'Twitter'
    GITHUB = 'github', 'Github'
    INSTAGRAM = 'instagram', 'Instagram'
    LINKEDIN = 'linkedin', 'Linkedin'
    EMAIL = 'email', _('Email')
    WEBSITE = 'site', _('Website')
    OTHER = 'other', _('Other')


class SocialLink(InvalidateCacheMixin, models.Model):
    speaker = ParentalKey(Speaker, on_delete=models.CASCADE,
                          related_name='social_links')
    type = models.CharField(max_length=16, choices=SocialLinkTypes.choices, default=SocialLinkTypes.OTHER,
                            verbose_name=_('type'))
    link = models.URLField(max_length=512, verbose_name=_('link'))

    @property
    def icon(self):
        return {
            SocialLinkTypes.FACEBOOK: 'fab fa-facebook',
            SocialLinkTypes.TWITTER: 'fab fa-twitter',
            SocialLinkTypes.GITHUB: 'fab fa-github',
            SocialLinkTypes.INSTAGRAM: 'fab fa-instagram',
            SocialLinkTypes.LINKEDIN: 'fab fa-linkedin',
            SocialLinkTypes.EMAIL: 'fas fa-envelope',
            SocialLinkTypes.WEBSITE: 'fas fa-link',
            SocialLinkTypes.OTHER: 'fas fa-external-link-alt',
        }.get(self.type, 'fas fa-external-link-alt')


class EditionIndex(SFIPage):
    subpage_types = ['Edition']

    EDITIONS_PER_PAGE = DEFAULT_PAGINATION

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = Edition.objects.live().public().descendant_of(
            self).order_by('-start_date', 'title')
        return context

    class Meta:
        verbose_name = _('edition index')
        verbose_name_plural = _('edition indexes')


class EditionSubpage(SFIPage):
    @abstractmethod
    def get_edition(self):
        pass

    @with_context
    def get_featured_image(self, context):
        if self.featured_image:
            return self.featured_image
        edition = self.get_edition()
        if edition.default_featured_image:
            return edition.default_featured_image
        return ThemeSettings.for_request(context['request']).default_featured_image

    def get_edition_footer(self):
        return self.get_edition().get_edition_footer()

    class Meta:
        abstract = True


class Edition(RoutablePageMixin, EditionSubpage):
    start_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_('edition start date'))
    end_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_('edition end date'))

    content = StreamField([
        ('agenda', AgendaBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('event_index', EventIndexBlock()),
        ('event_schedule', EventScheduleBlock()),
        ('section_title', SectionTitleBlock()),
        ('section_subtitle', SectionSubtitleBlock()),
        ('section_divider', SectionDividerBlock()),
        ('dropdown', DropdownBlock()),
        ('photo_gallery', PhotoGallery()),
        ('map', MapBlock()),
        ('raw_html', RawHTMLBlock()),
    ], null=True, blank=True, verbose_name=_('content'))

    default_featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('default featured image')
    )
    edition_footer = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('section_title', SectionTitleBlock()),
        ('section_subtitle', SectionSubtitleBlock()),
        ('section_divider', SectionDividerBlock()),
        ('dropdown', DropdownBlock()),
        ('photo_gallery', PhotoGallery()),
        ('raw_html', blocks.RawHTMLBlock()),
    ], null=True, blank=True, verbose_name=_('edition footer'))

    generate_podcast_feed = models.BooleanField(
        default=False, verbose_name=_('generate podcast feed'))

    def get_edition_footer(self):
        return self.edition_footer

    def get_edition(self):
        return self

    content_panels = SFIPage.content_panels + [
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        StreamFieldPanel('content'),
        ImageChooserPanel('default_featured_image'),
        InlinePanel('event_categories', label='Event categories'),
        StreamFieldPanel('edition_footer'),
    ]

    settings_panels = SFIPage.settings_panels + [
        FieldPanel('generate_podcast_feed')
    ]

    parent_page_types = ['EditionIndex']
    subpage_types = ['EventIndex']

    class Meta:
        verbose_name = _('edition')
        verbose_name_plural = _('editions')

    @route(r'^c/([\w\-_]+)/$')
    def get_category_event_index(self, request, category_name):
        indexes = EventIndex.objects.child_of(self).live().all()
        categories = Category.objects.filter(edition=self).order_by('name').all()
        category = categories.filter(slug=category_name).first()
        if not category:
            raise Http404
        events = Event.objects.live().public().descendant_of(self).filter(
            event_category=category).order_by('date')
        posts = paginate(events, request, EventIndex.EVENTS_PER_PAGE)
        relative_url = self.reverse_subpage('get_category_event_index', (category_name,))
        return TemplateResponse(request, 'agenda/event_index.html', {
            'posts': posts,
            'indexes': indexes,
            'categories': categories,
            'title': '{} - {}'.format(category.name, self.title),
            'description': '{} - {}'.format(category.name, self.title),
            'canonical_url': self.full_url + relative_url,
            'featured_image': self.get_featured_image(),
            'locales': [(lang_code, lang_name, url + relative_url, full_url + relative_url) for
                        lang_code, lang_name, url, full_url in self._get_locales()],
        })


class Category(InvalidateCacheMixin, models.Model):
    edition = ParentalKey(Edition, on_delete=models.CASCADE,
                          related_name='event_categories', verbose_name=_('edition'))
    name = models.CharField(max_length=100, verbose_name=_('name'))
    slug = models.CharField(max_length=100, verbose_name=_('slug'))
    icon = models.CharField(max_length=300, verbose_name=_('icon'))
    color = models.CharField(max_length=7,
                             default='#23211f',
                             validators=[RegexValidator(
                                 regex=r'^#([0-9a-fA-F]{6})$',
                                 message=_('Color must be in hex'),
                             ), ], verbose_name=_('color'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        copy_multi_lang(self, 'name', self, 'slug', slugify)
        super().save(force_insert, force_update, using, update_fields)

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('color', widget=TextInput(
            attrs={'type': 'color', 'style': 'height:60px'}))
    ]

    @property
    def url(self):
        return self.edition.url + self.edition.reverse_subpage('get_category_event_index', (self.slug,))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('event category')
        verbose_name_plural = _('event categories')


class EventIndex(EditionSubpage):
    parent_page_types = ['Edition']
    subpage_types = ['Event']

    EVENTS_PER_PAGE = DEFAULT_PAGINATION

    color = models.CharField(max_length=7,
                             default='#23211f',
                             validators=[RegexValidator(
                                 regex=r'^#([0-9a-fA-F]{6})$',
                                 message=_('Color must be in hex'),
                             ), ], verbose_name=_('color'))
    reversed_order = models.BooleanField(
        default=False, verbose_name=_('reversed index order'))

    content_panels = SFIPage.content_panels + [
        FieldPanel('reversed_order'),
        FieldPanel('color', widget=TextInput(
            attrs={'type': 'color', 'style': 'height:60px'})),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        events = Event.objects.live().public().descendant_of(
            self).order_by('-date' if self.reversed_order else 'date')
        context['posts'] = paginate(
            events, request, EventIndex.EVENTS_PER_PAGE)
        context['categories'] = Category.objects.filter(edition=self.get_edition()).order_by(
            'name').all()
        context['indexes'] = EventIndex.objects.child_of(self.get_edition()).live().all()

        return context

    def get_edition(self):
        return self.get_parent().edition

    class Meta:
        verbose_name = _('event list')
        verbose_name_plural = _('event lists')


class LanguageChoice(models.TextChoices):
    POLISH = 'pl', _('Polish')
    ENGLISH = 'en', _('English')
    POLISH_ENGLISH = 'pl+en', _('Polish+English')


class Event(EditionSubpage):
    content = RichTextField(verbose_name=_('content'))
    date = models.DateTimeField(null=True, blank=True, verbose_name=_('date'))
    duration_minutes = models.IntegerField(
        null=True, blank=True, verbose_name=_('duration in minutes'))
    event_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL,
                                       verbose_name=_('category'))
    language = models.CharField(max_length=5, choices=LanguageChoice.choices, null=True, blank=True,
                                verbose_name=_('language'))
    sponsor = models.ForeignKey(
        Sponsor, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('sponsor'))
    recording_link = models.URLField(
        max_length=512, null=True, blank=True, verbose_name=_('link to recording'))
    audio_recording = models.ForeignKey(AudioFile, null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name=_('audio recording file'))

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
        InlinePanel('event_speakers', label='Event speakers'),
        EventCategoryFieldPanel('event_category'),
        FieldPanel('language'),
        SnippetChooserPanel('sponsor'),
        FieldPanel('recording_link'),
        SnippetChooserPanel('audio_recording'),
    ]

    parent_page_types = ['EventIndex']
    subpage_types = []

    def index(self):
        return self.get_parent().eventindex

    def get_type(self):
        return self.index().title

    def get_edition(self):
        return self.get_parent().get_parent().edition

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class EventSpeaker(InvalidateCacheMixin, models.Model):
    event = ParentalKey(Event, on_delete=models.CASCADE,
                        related_name='event_speakers')
    speaker = models.ForeignKey(Speaker, null=True, on_delete=models.PROTECT, verbose_name=_('speaker'),
                                related_name='event_speakers')

    panels = [
        PageChooserPanel('speaker'),
    ]

    @property
    def live(self):
        return self.event.live and self.speaker.live

    class Meta:
        verbose_name = _('event speaker')
        verbose_name_plural = _('event speakers')
