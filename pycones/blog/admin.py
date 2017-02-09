# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from pycones.blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'status']
    list_filter = ('status',)
