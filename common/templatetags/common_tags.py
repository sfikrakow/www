from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter, truncatewords
from django.utils.html import strip_tags

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def unrich_text(value):
    value = value.replace('<p>', '').replace('</p>', ' ')
    return strip_tags(value)


@register.inclusion_tag('common/tags/responsive_img.html')
def responsive_img(img, size: str, css_class=''):
    if img:
        image_jpg = img.get_rendition(size + '|format-jpeg|jpegquality-70')
        image_webp = img.get_rendition(size + '|format-webp')
        return {
            'image_jpg': image_jpg,
            'image_webp': image_webp,
            'css_class': css_class,
        }
    else:
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


@register.inclusion_tag('common/tags/responsive_img.html', takes_context=True)
def responsive_featured_image(context, page, size: str, css_class=''):
    return responsive_img(page.get_featured_image_or_default(context), size, css_class)


@register.simple_tag(takes_context=True)
def get_featured_image_url(context, page):
    image = page.get_featured_image_or_default(context)
    if image:
        rendition = image.get_rendition('max-1200x1200|format-jpeg|jpegquality-70')
        return context['request'].build_absolute_uri(rendition.url)
    return ''


@register.simple_tag
def page_languages(page):
    locales = [x[0] for x in settings.LANGUAGES if page.__dict__['slug_' + x[0]]]
    return locales
