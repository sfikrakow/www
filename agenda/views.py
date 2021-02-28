# Create your views here.
import os

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import truncatechars, slugify
from django.utils import translation
from django.utils.feedgenerator import Rss201rev2Feed, rfc2822_date
from wagtail.images.models import Image

from agenda.models import Edition, Event
from common.templatetags.common_tags import unrich_text
from common.utils import RenderWithContext


class ITunesFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super().rss_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        return attrs

    def root_attributes(self):
        attrs = super().root_attributes()
        return attrs

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.addQuickElement("pubDate", rfc2822_date(self.latest_post_date()))
        handler.addQuickElement('itunes:summary', self.feed['description'])
        handler.addQuickElement('itunes:subtitle', truncatechars(self.feed['description'], 49))
        handler.addQuickElement('itunes:author', self.feed['author_name'])
        handler.addQuickElement('itunes:explicit', self.feed['explicit'])
        handler.addQuickElement('itunes:category', attrs={'text': self.feed['itunes_category']})
        handler.startElement('itunes:owner', {})
        handler.addQuickElement('itunes:name', self.feed['owner_name'])
        handler.addQuickElement('itunes:email', self.feed['owner_email'])
        handler.endElement('itunes:owner')
        handler.addQuickElement('itunes:image', attrs={'href': self.feed['image_url']})
        handler.addQuickElement('webMaster', self.feed['webMaster'])
        handler.startElement('image', {})
        handler.addQuickElement('url', self.feed['image_url'])
        handler.addQuickElement('title', self.feed['title'])
        handler.addQuickElement('link', self.feed['link'])
        handler.endElement('image')

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement('itunes:summary', item['description'])
        handler.addQuickElement('itunes:subtitle', truncatechars(item['description'], 49))
        handler.addQuickElement('itunes:duration', item['duration'])
        handler.addQuickElement('itunes:explicit', item['explicit'])
        handler.addQuickElement('itunes:image', attrs={'href': item['image_url']})
        handler.addQuickElement('itunes:author', self.feed['author_name'])


def _merge_multi_lang(obj, base_field_name):
    texts = []
    for lang, _ in settings.LANGUAGES:
        field_name = '{}_{}'.format(base_field_name, lang)
        if hasattr(obj, field_name) and getattr(obj, field_name):
            texts.append('[{}] {}'.format(lang.upper(), unrich_text(getattr(obj, field_name))))
    return ' \n'.join(texts)


def _podcast_image(context, img):
    if isinstance(img, RenderWithContext):
        img = img.render(context)
    if isinstance(img, Image):
        rendition = img.get_rendition('fill-1500x1500|format-jpeg|jpegquality-70')
        return context['request'].build_absolute_uri(rendition.url)
    return ''


class EditionPodcastFeedView(Feed):
    feed_type = ITunesFeed
    model = Edition

    def __call__(self, request, *args, **kwargs):
        translation.deactivate_all()
        self.request = request
        self.context = {'request': request}
        return super().__call__(request, *args, **kwargs)

    def get_object(self, request, *args, **kwargs):
        if 'slug' not in kwargs:
            raise Http404()
        return get_object_or_404(Edition, slug=kwargs['slug'], generate_podcast_feed=True)

    def link(self, obj):
        return obj.url

    def title(self, obj):
        return obj.seo_title if obj.seo_title else obj.title

    def description(self, obj):
        return _merge_multi_lang(obj, 'search_description')

    def items(self, obj):
        return Event.objects.descendant_of(obj).live().exclude(audio_recording__isnull=True).exclude(
            date__isnull=True).exclude(audio_recording__duration_seconds__lt=0).all()

    def item_link(self, item):
        return item.url

    def item_guid(self, item):
        if item.audio_recording.guid_override:
            return item.audio_recording.guid_override
        return 'SFIKRAKOW:track/{}/{}'.format(item.audio_recording.id,
                                              os.path.basename(slugify(item.audio_recording.file.name)))

    def item_enclosure_url(self, item):
        return self.request.build_absolute_uri(item.audio_recording.file.url)

    def item_enclosure_length(self, item):
        return item.audio_recording.file.size

    def item_enclosure_mime_type(self, item):
        return item.audio_recording.mime_type

    def item_description(self, item):
        return _merge_multi_lang(item, 'content')

    def item_pubdate(self, item):
        return max(item.audio_recording.modification_date, item.last_published_at)

    item_guid_is_permalink = False
    language = 'en'
    feed_copyright = 'All rights reserved'
    ttl = 60
    author_name = 'SFI Academic IT Festival'

    def feed_extra_kwargs(self, obj):
        return {
            'webMaster': 'podcast@sfi.pl',
            'explicit': 'no',
            'owner_name': 'SFI Academic IT Festival',
            'owner_email': 'podcast@sfi.pl',
            'image_url': _podcast_image(self.context, obj.get_featured_image()),
            'itunes_category': 'Technology',
        }

    def item_extra_kwargs(self, item):
        return {
            'explicit': 'yes' if item.audio_recording.explicit_content else 'no',
            'duration': str(item.audio_recording.duration_seconds),
            'image_url': _podcast_image(self.context, item.get_featured_image()),
        }
