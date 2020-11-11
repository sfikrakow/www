import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.utils.cache import get_conditional_response, get_cache_key, learn_cache_key
from django.utils.http import http_date
from wagtail.core.models import Page
from django.core.cache import cache

LAST_MODIFIED_KEY = 'last_modified_date'
CACHE_PREFIX = 'PageCache'
CACHE_MAX_TTL = 7 * 60 * 60 * 24
PAGE_MAX_TTL = 60 * 60 * 24


def update_last_modified_stamp(last_modified=timezone.now()):
    cache.set(LAST_MODIFIED_KEY, last_modified, CACHE_MAX_TTL)


def get_last_modified_stamp():
    last_modified = cache.get_or_set(LAST_MODIFIED_KEY, timezone.now(), CACHE_MAX_TTL)
    return last_modified


class InvalidateCacheMixin(models.Model):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        ret = super().save(force_insert, force_update, using, update_fields)
        update_last_modified_stamp()
        return ret

    class Meta:
        abstract = True


def _is_request_cacheable(request: HttpRequest) -> bool:
    return request.method in ('GET', 'HEAD') and not getattr(request, 'is_preview', False) and not (
            hasattr(request, 'user') and request.user.is_authenticated)


def _is_page_cacheable(page: Page):
    if page.get_view_restrictions():
        return False
    return True


@dataclass
class CacheEntry:
    response: HttpResponse
    created_date: datetime


def _try_get_cache(request: HttpRequest) -> Optional[CacheEntry]:
    cache_key = get_cache_key(request, CACHE_PREFIX, 'GET', cache=cache)
    if cache_key is None:
        return None
    entry = cache.get(cache_key)
    if entry is None and request.method == 'HEAD':
        cache_key = get_cache_key(request, CACHE_PREFIX, 'HEAD', cache=cache)
        entry = cache.get(cache_key)
    return entry


def _store_cache(request: HttpRequest, response: HttpResponse):
    cache_key = learn_cache_key(request, response, PAGE_MAX_TTL, CACHE_PREFIX, cache=cache)
    entry = CacheEntry(response, timezone.now())
    cache.set(cache_key, entry, PAGE_MAX_TTL)


def cache_page(request: HttpRequest, page: Page, response_fs):
    if not _is_request_cacheable(request) or not _is_page_cacheable(page) or settings.DEBUG:
        response = response_fs()
        response['Cache-Control'] = 'max-age=0, private, must-revalidate'
        return response
    last_modified = get_last_modified_stamp()
    last_modified_stamp = http_date(last_modified.timestamp())
    md5 = hashlib.md5(request.get_full_path().encode('utf-8'))
    md5.update(last_modified_stamp.encode('utf-8'))
    etag = 'W/"{}"'.format(md5.hexdigest())

    # Try getting a Not Modified response.
    response = get_conditional_response(request, etag, last_modified)
    if response:
        return response

    # Lookup cache
    entry = _try_get_cache(request)
    if entry and entry.created_date > last_modified:
        return entry.response

    # render page
    response = response_fs()

    # Cache rendered page on success
    if response.status_code != 200:
        return response
    response['Last-Modified'] = last_modified_stamp
    response['ETag'] = etag
    response['Cache-Control'] = 'max-age=0, public, s-maxage=60'
    response.add_post_render_callback(lambda rendered: _store_cache(request, rendered))
    return response
