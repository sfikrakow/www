from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_captcha_public_key():
    return settings.RECAPTCHA_PUBLIC_KEY
