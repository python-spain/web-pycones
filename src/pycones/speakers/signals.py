# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.contrib.auth.models import Group

from pycones.speakers import SPEAKERS_GROUP_NAME
from pycones.speakers.models import Speaker


def register_speakers_handler(sender, **kwargs):
    """Handle profiles when the user is added to a group."""

    action = kwargs.get("action")
    instance = kwargs.get("instance")
    if instance and action in ("post_add", "post_remove"):
        if SPEAKERS_GROUP_NAME in instance.groups.values_list("name", flat=True):
            if not Speaker.objects.filter(user=instance).exists():
                Speaker.objects.create(user=instance)
        else:
            if Speaker.objects.filter(user=instance).exists():
                Speaker.objects.filter(user=instance).delete()


def create_speakers_group(sender, **kwargs):
    """Creates speakers group."""

    if not Group.objects.filter(name=SPEAKERS_GROUP_NAME).exists():
        Group.objects.create(name=SPEAKERS_GROUP_NAME)
