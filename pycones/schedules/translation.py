# -*- coding: utf-8 -*-

from modeltranslation.translator import register, TranslationOptions

from pycones.schedules.models import Room, SlotKind, Presentation, Slot, Track


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(SlotKind)
class SlotKindTranslationOptions(TranslationOptions):
    fields = ("label",)


@register(Presentation)
class PresentationTranslationOptions(TranslationOptions):
    fields = ("title", "description", "abstract")


@register(Slot)
class SlotTranslationOptions(TranslationOptions):
    fields = ("content_override",)


@register(Track)
class TrackTranslationOptions(TranslationOptions):
    fields = ("name",)
