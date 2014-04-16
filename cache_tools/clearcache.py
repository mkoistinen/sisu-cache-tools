# -*- coding: utf-8 -*-

from django.contrib.sitemaps import ping_google
from django.core.cache import cache
from django.db.models.signals import post_save, m2m_changed
from django.core.signals import request_started

from cms.models import CMSPlugin

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
