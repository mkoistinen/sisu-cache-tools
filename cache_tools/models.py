# -*- coding: utf-8 -*-

#
# NOTE: This project doesn't use models. However, clearcache.* needs to be
# loaded at load time in order for the signals to work properly, and loading
# them here in models.py appears to be "best practice".
#
# As of Django 1.7, we *also* do this in apps.py, but we continue to do it
# here––wrapped in try/except––for Djangos < 1.7
#

try:
	from .clearcache import *
except:
	pass