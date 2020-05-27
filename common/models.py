from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class User(AbstractUser):
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class SFIPage(Page):
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('featured image')
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('featured_image'),
    ]

    class Meta:
        abstract = True
