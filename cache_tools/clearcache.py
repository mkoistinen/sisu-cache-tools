# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.core.cache import cache
from django.core.signals import request_started
from django.db.models.signals import post_save, m2m_changed

from cms.models import CMSPlugin

import requests

#
# This sets up the domain that will be BANned from the Varnish caches.
#
if hasattr(settings, 'SITE_ID'):
    DOMAIN = Site.objects.get_current()

    #
    # The HOST_URL isn't really used for the BANning process, but it does need
    # to be something that will be accepted by Varnish, otherwise Varnish will
    # let Nginx handle the request.
    #
    HOST_URL = 'http://{0}/'.format(DOMAIN)

#
# It is the proxy setting that determines WHERE the BAN will be sent. So,
# we'll loop through the list of configured settings.CACHE_SERVERS and, one-
# by-one, send the BAN request (a DELETE verb, really, since Requests can't
# seem to handle a custom HTTP verb).
#

#
# This is a general purpose handler for managing our cache-clearing In order
# for this to work, the attribute 'taints_cache' must be set to True on models
# that, when changed, may affect the output of pages in the system. CMSPlugin
# models do not need this attribute, as they are already included. When any of
# these models are saved, the cache will be cleared. If a M2M relationship
# involving one of these taints_cache models changes, the cache will be
# cleared.
#
# Also, in order to be more efficient, we attempt to minimize the number of
# cache-clearings to only as necessary. In order to do this, we listen for
# request events and mark the cache as rebuilt when a page is requested. If
# the cache is NOT rebuilt, we don't bother clearing the cache again.
#

class CacheClearer:
    rebuilt = True

    @classmethod
    def ping_google(cls):
        try:
            ping_google()
        except Exception:
            pass

    @classmethod
    def clear(cls):
        if cls.rebuilt:
            cache.clear()

            if hasattr(settings, 'SITE_ID') and hasattr(settings, 'CACHE_SERVERS'):
                for proxy in settings.CACHE_SERVERS:
                    req = requests.delete(HOST_URL, headers={
                        'X-Ban-Host': DOMAIN,
                    }, proxies={ 'http': proxy })
                    if not req.status_code == 200:
                        print('BAN request to cache server: {0} returned a status code of {1}'.format(
                            proxy,
                            req.status_code
                        ))

            cls.rebuilt = False

    @classmethod
    def modelClear(cls, sender, **kwargs):
        if (
            isinstance(sender, CMSPlugin) or
            'taints_cache' in sender.__dict__ and sender.taints_cache
        ):
            cls.ping_google()
            cls.clear()

    @classmethod
    def m2mClear(cls, sender, instance, model, **kwargs):
        if (
            isinstance(sender, CMSPlugin) or
            'taints_cache' in instance.__class__.__dict__ and
                instance.__class__.taints_cache or
            'taints_cache' in model.__dict__ and model.taints_cache
        ):
            cls.ping_google()
            cls.clear()

    @classmethod
    def mark_rebuilt(cls, sender, **kwargs):
        if not cls.rebuilt:
            cls.rebuilt = True


post_save.connect(CacheClearer.modelClear)
m2m_changed.connect(CacheClearer.m2mClear)
request_started.connect(CacheClearer.mark_rebuilt)
