# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import six
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from pycones.configurations import TYPE_CHOICES, STRING, INT, FLOAT
from pycones.configurations.managers import OptionManager


@python_2_unicode_compatible
class Option(models.Model):
    """System options and configurations."""

    name = models.CharField(
        verbose_name=_("Parameter"),
        max_length=255,
        unique=True,
        db_index=True
    )
    public_name = models.CharField(
        verbose_name=_("Public name of the parameter"),
        max_length=255,
        unique=False,
        db_index=True
    )
    type = models.PositiveIntegerField(
        choices=TYPE_CHOICES,
        default=STRING
    )
    value = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=256,
        verbose_name=_("Value")
    )

    is_list = models.BooleanField(default=False)

    objects = OptionManager()

    def __str__(self):
        return "%s" % self.public_name

    def get_value(self):
        """Gets the value with the proper type."""
        converter = {
            INT: int,
            FLOAT: float,
            STRING: six.text_type
        }
        if not self.is_list:
            return converter.get(self.type, six.text_type)(self.value)
        else:
            values = self.value.split(",")
            return list(map(lambda item: converter.get(self.type, six.text_type)(item), values))
