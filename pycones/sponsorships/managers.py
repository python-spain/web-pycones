# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class SponsorManager(models.Manager):

    def active(self):
        return self.get_query_set().filter(active=True).order_by("level")
