from django.conf import settings
from django.http import HttpResponse


def sitemap_index(request):
    map = '''<?xml version="1.0" encoding="UTF-8"?>
  <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{}
  </sitemapindex>
    '''.format(''.join('''
    <sitemap>
      <loc>{}</loc>
    </sitemap>
    '''.format(request.build_absolute_uri('/{}/sitemap.xml'.format(x))) for x, _ in settings.LANGUAGES))
    return HttpResponse(map, content_type='application/xml')
