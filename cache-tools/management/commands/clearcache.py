# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from ...clearcache import CacheClearer

class Command(BaseCommand):

    help='''Clears the cache.'''

    def handle(self, *args, **kwargs):
        CacheClearer.clear()
        self.stdout.write('Cleared cache\n')
