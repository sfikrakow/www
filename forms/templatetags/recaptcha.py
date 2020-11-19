from captcha.constants import TEST_PUBLIC_KEY
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_captcha_public_key():
    return getattr(settings, "RECAPTCHA_PUBLIC_KEY", TEST_PUBLIC_KEY)
