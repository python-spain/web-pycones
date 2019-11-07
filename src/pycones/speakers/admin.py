# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from pycones.speakers.actions import download_approved_speakers
from pycones.speakers.models import Speaker
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Speaker)
class SpeakerAdmin(TabbedTranslationAdmin):
    list_display = ["name", "email", "created"]
    search_fields = ["name"]
    actions = [download_approved_speakers]

