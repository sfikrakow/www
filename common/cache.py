import hashlib
from calendar import timegm
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.utils.cache import get_conditional_response, _generate_cache_key
from django.utils.http import http_date

LAST_MODIFIED_KEY = 'last_modified_date'
CACHE_PREFIX = 'PageCache'
CACHE_MAX_TTL = 7 * 60 * 60 * 24
PAGE_MAX_TTL = 60 * 60 * 24
SFI_CACHE_HEADER = 'X-SFI-Cache'


def update_last_modified_stamp(last_modified=None):
    cache.set(LAST_MODIFIED_KEY, last_modified if last_modified else timezone.now(), CACHE_MAX_TTL)


def get_last_modified_stamp() -> datetime:
    return cache.get_or_set(LAST_MODIFIED_KEY, timezone.now(), CACHE_MAX_TTL)


def get_last_modified_and_etag(request: HttpRequest):
    last_modified_stamp = http_date(timegm(get_last_modified_stamp().utctimetuple()))
    md5 = hashlib.md5(request.get_full_path().encode('utf-8'))
    md5.update(last_modified_stamp.encode('utf-8'))
    etag = 'W/"{}"'.format(md5.hexdigest())
    return last_modified_stamp, etag


class InvalidateCacheMixin(models.Model):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        ret = super().save(force_insert, force_update, using, update_fields)
        update_last_modified_stamp()
        return ret

    class Meta:
        abstract = True


@dataclass
class CacheEntry:
    response: HttpResponse
    created_date: datetime


PAGE_CACHE_URLS = ('/en/', '/pl/')


class FetchPageFromCacheMiddleware:
    """Cache for SFI pages,"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if settings.DEBUG:
            response = self.get_response(request)
            response['Cache-Control'] = 'max-age=0, private, must-revalidate'
            response[SFI_CACHE_HEADER] = 'DEBUG_BYPASS'
            return response

        if not request.path.startswith(PAGE_CACHE_URLS) or not self._is_request_cacheable(request):
            response = self.get_response(request)
            response['Cache-Control'] = 'max-age=0, private, must-revalidate'
            response[SFI_CACHE_HEADER] = 'BYPASS'
            return response

        last_modified = get_last_modified_stamp()
        last_modified_stamp, etag = get_last_modified_and_etag(request)

        # Try getting a Not Modified response.
        response = get_conditional_response(request, etag, timegm(last_modified.utctimetuple()))
        if response:
            response[SFI_CACHE_HEADER] = 'NON_MODIFIED'
            return response

        # Lookup cache
        entry = self._try_get_cache(request)
        if entry and entry.created_date > last_modified:
            response = entry.response
            response[SFI_CACHE_HEADER] = 'HIT'
            return response

        request._cache_update_cache = True
        response = self.get_response(request)
        response[SFI_CACHE_HEADER] = 'MISS'
        return response

    @staticmethod
    def _try_get_cache(request: HttpRequest) -> Optional[CacheEntry]:
        cache_key = _generate_cache_key(request, 'GET', [], CACHE_PREFIX)
        if cache_key is None:
            return None
        entry = cache.get(cache_key)
        if entry is None and request.method == 'HEAD':
            cache_key = _generate_cache_key(request, 'HEAD', [], CACHE_PREFIX)
            entry = cache.get(cache_key)
        return entry

    @staticmethod
    def _is_request_cacheable(request: HttpRequest) -> bool:
        return request.method in ('GET', 'HEAD') and not getattr(request, 'is_preview', False) and not (
                hasattr(request, 'user') and request.user.is_authenticated)


# noinspection PyProtectedMember,PyUnresolvedReferences
class UpdatePageCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        if not (hasattr(request, '_cache_update_cache') and request._cache_update_cache):
            return response

        if response.streaming or response.status_code != 200:
            return response

        last_modified_stamp, etag = get_last_modified_and_etag(request)

        response['Last-Modified'] = last_modified_stamp
        response['ETag'] = etag
        response['Cache-Control'] = 'max-age=0, public, s-maxage=60'

        cache_key = _generate_cache_key(request, request.method, [], CACHE_PREFIX)
        if hasattr(response, 'render') and callable(response.render):
            response.add_post_render_callback(
                lambda rendered: cache.set(cache_key, CacheEntry(rendered, timezone.now()), PAGE_MAX_TTL)
            )
        else:
            cache.set(cache_key, CacheEntry(response, timezone.now()), PAGE_MAX_TTL)
        return response
