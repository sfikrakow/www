from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def unrich_text(value):
    value = value.replace('<p>', '').replace('</p>', ' ')
    return strip_tags(value)
