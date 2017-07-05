# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import ugettext_lazy as _

from pycones.schedules.models import Day, Room, SlotKind, Slot, Presentation, Track


@admin.register(Slot)
class SlotAdmin(ModelAdmin):
    list_display = ("id", "day", "start", "end", "kind", "room", "order", "get_content_title")

    def get_content_title(self, instance):
        if instance.content:
            return instance.content.get_title()
        return None
    get_content_title.short_description = _("Title")


@admin.register(Track)
class TrackAdmin(ModelAdmin):
    list_display = ("id", "day", "name")


admin.site.register(Day)
admin.site.register(Room)
admin.site.register(SlotKind)
admin.site.register(Presentation)


