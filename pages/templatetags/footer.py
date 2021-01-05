from django import template

from pages.models import FooterSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_footer(context, page):
    if hasattr(page, 'get_edition_footer'):
        footer = page.get_edition_footer()
    else:
        footer = FooterSettings.for_request(context['request']).content
    return footer if footer else ''
