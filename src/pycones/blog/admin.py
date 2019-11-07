# -*- coding: utf-8 -*-

from django.contrib import admin

from pycones.blog.models import Post
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Post)
class PostAdmin(TabbedTranslationAdmin):
    list_display = ["id", "title", "created", "status"]
    list_filter = ("status",)
