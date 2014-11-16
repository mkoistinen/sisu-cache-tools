# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.core.signals import request_started
from django.db.models.signals import post_save, m2m_changed
from django.utils.translation import ugettext_lazy as _


class CacheToolsConfig(AppConfig):
    name = 'cache_tools'
    verbose_name = _("Sisu Cache Tools")

    def ready(self):
        from .clearcache import CacheClearer

        #
        # Handle signals
        #
        post_save.connect(CacheClearer.modelClear)
        m2m_changed.connect(CacheClearer.m2mClear)
        request_started.connect(CacheClearer.mark_rebuilt)
