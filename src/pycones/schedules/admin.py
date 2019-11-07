# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pycones.schedules.actions import download_speakers, create_slots
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
        "track",
        "order",
        "content",
    )
    actions = [create_slots]
    list_filter = ["day", "room", "kind"]
    list_editable = ["order", "room"]


@admin.register(Track)
class TrackAdmin(TabbedTranslationAdmin):
    list_display = ("id", "day", "name", "order")
    list_filter = ("day",)
    list_editable = ("order",)


@admin.register(Presentation)
class PresentationAdmin(TabbedTranslationAdmin):
    actions = [download_speakers]
    list_display = ["id", "title", "slot", "slot_id"]
    raw_id_fields = ["slot"]
    search_fields = ["title"]

    def slot_id(self, obj):
        try:
            return obj.slot.id
        except:
            return "-"

    slot_id.short_description = "Slot"
    slot_id.admin_order_field = "slot__id"


@admin.register(Room)
class RoomAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name")


@admin.register(SlotKind)
class SlotKindAdmin(TabbedTranslationAdmin):
    list_display = ("id", "label")


admin.site.register(Day)
