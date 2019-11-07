# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import sys
from importlib import reload, import_module

from django.conf import settings
from django.urls import set_urlconf


def reload_urlconf(urlconf=None, urls_attr='urlpatterns'):
    """Helper to reload urls, in order to test changes on settings that affects
    the urls.

    Source: https://gist.github.com/anentropic/9ac47f6518c88fa8d2b0
    """
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
    reloaded = import_module(urlconf)
    reloaded_urls = getattr(reloaded, urls_attr)
    set_urlconf(tuple(reloaded_urls))
