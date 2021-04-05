import importlib
import os
import re

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter, truncatechars
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from wagtail.images.models import Image

from common.image_preset import ImageRenderPreset, ImagePresets
from common.utils import RenderWithContext

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def unrich_text(value):
    value = value.replace('</p>', ' ').replace('<br/>', ' ')
    value = re.sub(r'</h\d>', ' ', value)
    return strip_tags(value)


@register.inclusion_tag('common/tags/responsive_img.html', takes_context=True)
def responsive_img(context, img, size: str, css_class='', placeholder=None, placeholder_webp=None, transparent=False):
    if isinstance(img, RenderWithContext):
        img = img.render(context)
    if isinstance(img, Image):
        if transparent:
            image = img.get_rendition(size + '|format-png')
        else:
            image = img.get_rendition(size + '|format-jpeg|jpegquality-70')
        image_webp = img.get_rendition(size + '|format-webp')
        return {
            'image': image.url,
            'image_webp': image_webp.url,
            'css_class': css_class,
            'alt': image.alt
        }
    if placeholder:
        return {
            'image': static(placeholder),
            'image_webp': static(placeholder_webp) if placeholder_webp else None,
            'css_class': css_class,
            'alt': 'placeholder'
        }
    return {}


@register.simple_tag(takes_context=True)
def responsive_img_set(context, img, preset_name: str, css_class='', placeholder=None, placeholder_webp=None):
    preset: ImageRenderPreset = ImagePresets[preset_name].value
    if isinstance(img, RenderWithContext):
        img = img.render(context)
    if isinstance(img, Image):
        sources = ''.join(
            '<source {media_query} srcset="{srcset}" type="{type}">'.format(
                media_query=('media="(min-width: {}px)"'.format(int(alternative.min_page_width_px)) if int(
                    alternative.min_page_width_px) > 0 else ''),
                srcset=','.join(
                    '{img} {dens}x'.format(
                        img=img.get_rendition(size + str(alternative.image_type.value[0])).url,
                        dens=dens
                    )
                    for size, dens in alternative.image_size_densities
                ),
                type=alternative.image_type.value[1]
            )
            for alternative in preset.image_alternatives
        )
        default_image = img.get_rendition(preset.default_image)
        tag = '<picture class="{css_class}">{sources}<img src="{default_image}" alt="{alt}"></picture>'.format(
            css_class=css_class,
            sources=sources,
            default_image=default_image.url,
            alt=default_image.alt
        )
        return mark_safe(tag)
    if placeholder:
        tag = '<picture class="{css_class}">{sources}<img src="{default_image}" alt="{alt}"></picture>'.format(
            css_class=css_class,
            sources='<source srcset="{img_webp}" type="image/webp">'.format(
                img_webp=static(placeholder_webp)) if placeholder_webp else '',
            default_image=static(placeholder),
            alt='placeholder'
        )
        return mark_safe(tag)
    return ''


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
        return mark_safe(truncatechars(unrich_text(page.content), 150))
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


@register.simple_tag
def fa_icon(fa_icon_string: str, icon_class: str = '', icon_style: str = '', icon_color: str = ''):
    match = re.fullmatch(r'^(\w{3}) fa-([A-Za-z-]+)$', fa_icon_string)
    if not match:
        return ''
    icon_type = {
        'fab': 'brands',
        'far': 'regular',
        'fas': 'solid',
    }.get(match.group(1), 'far')
    icon_name = match.group(2)

    fa = importlib.import_module("fontawesome-free")
    icons_path = os.path.dirname(fa.__file__)
    path = os.path.join(icons_path, 'static', 'fontawesome_free', 'svgs', icon_type, icon_name + '.svg')

    if icon_color:
        icon_style += 'color: ' + icon_color
    try:
        with open(path, 'r') as file:
            return mark_safe(
                '<span class="fa-icon {}" style="{}">{}</span>'.format(icon_class, icon_style, file.read()))
    except OSError:
        return ''
