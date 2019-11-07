# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.contrib.auth.models import Group

from pycones.reviewers import REVIEW_GROUP_NAME
from pycones.reviewers.models import Reviewer


def register_reviews_handler(sender, **kwargs):
    """Handle profiles when the user is added to a group."""

    action = kwargs.get("action")
    instance = kwargs.get("instance")
    if instance and action in ("post_add", "post_remove"):
        if REVIEW_GROUP_NAME in instance.groups.values_list("name", flat=True):
            if not Reviewer.objects.filter(user=instance).exists():
                Reviewer.objects.create(user=instance)
        else:
            if Reviewer.objects.filter(user=instance).exists():
                Reviewer.objects.filter(user=instance).delete()


def create_reviewers_group(sender, **kwargs):
    """Creates review group."""

    if not Group.objects.filter(name=REVIEW_GROUP_NAME).exists():
        Group.objects.create(name=REVIEW_GROUP_NAME)
