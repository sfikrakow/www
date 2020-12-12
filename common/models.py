from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel

from common.cache import InvalidateCacheMixin
from common.utils import with_context


class User(AbstractUser):
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class SFIPage(Page, InvalidateCacheMixin):
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('featured image')
    )

    @with_context
    def get_featured_image(self, context):
        if self.featured_image:
            return self.featured_image
        else:
            return ThemeSettings.for_request(context['request']).default_featured_image

    @with_context
    def get_edition_image(self, context):
        return ThemeSettings.for_request(context['request']).default_edition_image

    @with_context
    def get_footer_image(self, context):
        return ThemeSettings.for_request(context['request']).default_footer_image

    content_panels = Page.content_panels + [
        ImageChooserPanel('featured_image'),
    ]

    class Meta:
        abstract = True


@register_setting(icon='list-ul')
class NavigationMenu(BaseSetting, ClusterableModel, InvalidateCacheMixin):
    panels = [
        InlinePanel('menu_items', label=_('menu items'))
    ]

    class Meta:
        verbose_name = _('navigation menu')
        verbose_name_plural = _('navigation menus')


class NavigationMenuEntry(Orderable, InvalidateCacheMixin, models.Model):
    menu = ParentalKey(NavigationMenu, on_delete=models.CASCADE, related_name='menu_items', verbose_name=_('menu item'))
    link_title = models.CharField(max_length=128, verbose_name=_('link title'))
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
        verbose_name=_('linked page'),
        help_text=_('Overrides the url field')
    )
    link_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('link url'),
        help_text=_('Overridden by linked page')
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True, verbose_name=_('open in new tab'))

    panels = [
        FieldPanel('link_title'),
        PageChooserPanel('link_page'),
        FieldPanel('link_url'),
        FieldPanel('open_in_new_tab'),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'


@register_setting(icon='view')
class ThemeSettings(BaseSetting, InvalidateCacheMixin):
    default_featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('default featured image')
    )

    default_edition_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('default edition image')
    )

    default_footer_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('default footer image')
    )

    slider_primary_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('default primary image')
    )

    slider_secondary_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('default secondary image')
    )

    panels = [
        ImageChooserPanel('default_featured_image'),
        ImageChooserPanel('default_edition_image'),
        ImageChooserPanel('default_footer_image'),
        ImageChooserPanel('slider_primary_image'),
        ImageChooserPanel('slider_secondary_image'),
    ]

    class Meta:
        verbose_name = _('theme settings')
