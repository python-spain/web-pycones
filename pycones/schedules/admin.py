# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pycones.schedules.actions import download_speakers
from pycones.schedules.models import Day, Room, SlotKind, Slot, Presentation, Track
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Slot)
class SlotAdmin(TabbedTranslationAdmin):
    list_display = (
        "id",
        "day",
        "start",
        "end",
        "kind",
        "room",
        "order",
        "get_content_title",
    )

    def get_content_title(self, instance):
        if instance.content:
            return instance.content.get_title()
        return None

    get_content_title.short_description = _("Title")


@admin.register(Track)
class TrackAdmin(TabbedTranslationAdmin):
    list_display = ("id", "day", "name")


@admin.register(Presentation)
class PresentationAdmin(TabbedTranslationAdmin):
    actions = [download_speakers]


@admin.register(Room)
class RoomAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name")


@admin.register(SlotKind)
class SlotKindAdmin(TabbedTranslationAdmin):
    list_display = ("id", "label")


admin.site.register(Day)
