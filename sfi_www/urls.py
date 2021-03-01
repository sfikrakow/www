from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from agenda.views import EditionPodcastFeedView
from common.views import sitemap_index
from forms.views import ContactFormView

urlpatterns = [
    path('oidc/', include('mozilla_django_oidc.urls')),

    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('contact_form/', ContactFormView.as_view()),
    path('feeds/podcasts/<slug:slug>/', EditionPodcastFeedView(), name='feeds_podcast'),
    path('sitemap.xml', sitemap_index)
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + i18n_patterns(
    path('sitemap.xml', sitemap),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
)
