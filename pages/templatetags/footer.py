from django import template

from pages.models import FooterSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_footer(context, page):
    if hasattr(page, 'get_edition_footer'):
        return page.get_edition_footer()
    else:
        return FooterSettings.for_request(context['request']).content
