# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "pycones.users"

    def ready(self):
        """Connects signals with their managers."""
        pass
