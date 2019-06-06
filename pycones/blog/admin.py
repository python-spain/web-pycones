# -*- coding: utf-8 -*-

from django.contrib import admin

from pycones.blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created", "status"]
    list_filter = ("status",)
