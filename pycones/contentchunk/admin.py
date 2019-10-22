from django.contrib import admin
from .models import Chunk
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Chunk)
class SpeakerAdmin(TabbedTranslationAdmin):
    list_display = ["name"]
    search_fields = ["name"]

