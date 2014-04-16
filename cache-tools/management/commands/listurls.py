# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from ...precache import precache

class Command(BaseCommand):

    help = 'Lists all of the URLs found in the sitemaps.'

    def handle(self, *args, **kwargs):
        for url in precache.populate():
            self.stdout.write(url)
