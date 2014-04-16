# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from ...precache import precache

class Command(BaseCommand):

    help = 'Makes HTTP Requests to all of the URLs found in the sitemaps.'

    def handle(self, *args, **kwargs):
        self.stdout.write(precache.precache_all())
