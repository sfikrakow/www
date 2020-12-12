from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter, truncatewords
from django.templatetags.static import static
from django.utils.html import strip_tags
from wagtail.images.models import Image

from common.utils import RenderWithContext

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def unrich_text(value):
    value = value.replace('<p>', '').replace('</p>', ' ')
    return strip_tags(value)


@register.inclusion_tag('common/tags/responsive_img.html', takes_context=True)
def responsive_img(context, img, size: str, css_class='', placeholder=None, placeholder_webp=None):
    if isinstance(img, RenderWithContext):
        img = img.render(context)
    if isinstance(img, Image):
        image_jpg = img.get_rendition(size + '|format-jpeg|jpegquality-70')
        image_webp = img.get_rendition(size + '|format-webp')
        return {
            'image_jpg': image_jpg.url,
            'image_webp': image_webp.url,
            'css_class': css_class,
            'alt': image_jpg.alt
        }
    if placeholder:
        return {
            'image_jpg': static(placeholder),
            'image_webp': static(placeholder_webp) if placeholder_webp else None,
            'css_class': css_class,
            'alt': 'placeholder'
        }
    return {}


@register.simple_tag
def get_title(page):
    if page.seo_title:
        return page.seo_title
    else:
        return page.title


@register.simple_tag
def get_description(page):
    if page.search_description:
        return page.search_description
    elif hasattr(page, 'content') and isinstance(page.content, str) and not page.content.startswith('{'):
        return truncatewords(unrich_text(page.content), 15)
    else:
        return ''


@register.simple_tag(takes_context=True)
def get_featured_image_url(context, img):
    if isinstance(img, RenderWithContext):
        img = img.render(context)
    if isinstance(img, Image):
        rendition = img.get_rendition('max-1200x1200|format-jpeg|jpegquality-70')
        return context['request'].build_absolute_uri(rendition.url)
    return ''


@register.simple_tag
def page_languages(page):
    locales = [x[0] for x in settings.LANGUAGES if page.__dict__['slug_' + x[0]]]
    return locales
