# -*- coding: utf-8 -*-

from importlib import import_module
import time
import urllib2

from django.conf import settings
from django.contrib.sites.models import Site


class PreCache(object):

    @classmethod
    def _get_sitemaps(cls):
        '''Gets the sitemaps dict from ROOT_URLCONF'''
        url_conf = import_module(settings.ROOT_URLCONF)

        if hasattr(url_conf, 'sitemaps'):
            return url_conf.sitemaps
        else:
            return dict()

    @classmethod
    def populate(cls):
        '''Returns a list of all URLs in the sitemaps.'''
        current_site = Site.objects.get_current()

        for name, sitemap_class in cls._get_sitemaps().iteritems():
            sitemap = sitemap_class()
            for item in sitemap.items():
                if hasattr(sitemap, 'location'):
                    url = sitemap.location(item)
                else:
                    url = item.get_absolute_url()

                if settings.DEBUG:
                    host = '127.0.0.1'
                    port = 8000
                else:
                    host = current_site.domain
                    port = 80

                if port == 80:
                    yield (u'http://%s%s' % (host, url, ))
                else:
                    yield (u'http://%s:%s%s' % (host, port, url, ))

    @classmethod
    def precache_all(cls):
        '''Requests all of the URLs found in the sitemaps.'''
        done = 0
        fail = 0
        start = time.time()

        for url in cls.populate():
            try:
                response = urllib2.urlopen(url)
                code = response.getcode()
                if not code == 200:
                    print(u'Fetched page(%s) returned: %s' % (url, response.code, ))
                done += 1
            except:
                print(u'Unable to fetch: %s' % url)
                fail =+ 1

        elapsed = time.time() - start
        return u'Precache complete. {0:,} pages fetched successfully, {1:,} pages fetched with errors. Elapsed time: {2:,.3f}s.'.format(done, fail, elapsed, )

precache = PreCache()
