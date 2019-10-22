# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from pycones.blog.views import PostsListView, PostsFeed, PostsAtomFeed

app_name = "blog"

urlpatterns = [
    url(r"^$", PostsListView.as_view(), name="list"),
    url(r"^feed/", PostsFeed(), name="blog_feed"),
    url(r"^atom/", PostsAtomFeed(), name="blog_atom"),
    url(r"^rss/", RedirectView.as_view(url=reverse_lazy("blog_feed"))),
]
