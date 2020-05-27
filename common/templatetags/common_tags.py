from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def unrich_text(value):
    value = value.replace('<p>', '').replace('</p>', ' ')
    return strip_tags(value)


@register.inclusion_tag('common/tags/responsive_img.html')
def responsive_img(img, size: str, css_class='', placeholder=''):
    if img:
        image_jpg = img.get_rendition(size + '|format-jpeg|jpegquality-70')
        image_webp = img.get_rendition(size + '|format-webp')
        return {
            'image_jpg': image_jpg,
            'image_webp': image_webp,
            'css_class': css_class,
        }
    else:
        # TODO: placeholder
        return {}
