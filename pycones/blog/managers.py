# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models

from pycones.blog import PUBLISHED


class ArticlesManager(models.Manager):
    """Manager for posts. handle articles."""

    def requested_objects(self, request, page=None, queryset=None):
        if not queryset:
            queryset = self.all()
        posts_list = queryset.filter(status=PUBLISHED).order_by("-created")
        paginator = Paginator(posts_list, 5)
        if page is None:
            page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return posts
