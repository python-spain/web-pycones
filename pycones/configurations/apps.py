# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import six
from django.apps import AppConfig
from django.db.models.signals import post_migrate

from pycones.configurations import DEFAULT_OPTIONS


def create_default_options(sender, **kwargs):
    """Creates the defaults configuration options if they don't exists."""
    from pycones.configurations.models import Option
    for key, data in six.iteritems(DEFAULT_OPTIONS):
        if not Option.objects.filter(name=key).exists():
            Option.objects.create(name=key, **data)


class ConfigurationsConfig(AppConfig):
    name = "pycones.configurations"

    def ready(self):
        """Connects signals with their managers."""
        post_migrate.connect(create_default_options)
