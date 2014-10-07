# -*- coding: utf-8 -*-

#
# NOTE: This project doesn't use models. However, clearcache.* needs to be
# loaded at load time in order for the signals to work properly, and loading
# them here in models.py appears to be "best practice".
#

from .clearcache import *