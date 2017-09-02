# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from pycones.speakers.actions import download_approved_speakers
from pycones.speakers.models import Speaker


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created"]
    search_fields = ["name"]
    actions = [download_approved_speakers]

