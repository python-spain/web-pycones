# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models


class OptionManager(models.Manager):
    """Manager for options."""

    def get_value(self, name, default=None):
        """Gets the value with the proper type."""
        try:
            option = self.model.objects.get(name=name)
            return option.get_value()
        except self.model.DoesNotExist:
            return default
