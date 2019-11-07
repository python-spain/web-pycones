# -*- coding: utf-8 -*-


from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from pycones.blog import PUBLISHED
from pycones.blog.models import Post


class PostsListView(View):
    """List of posts."""

    @staticmethod
    def get(request):
        posts = Post.objects.requested_objects(request)
        return render(request, "blog/list.html", {"posts": posts})


class PostDetailsView(View):
    """Detail of a post."""

    @staticmethod
    def get(request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, "blog/details.html", {"post": post})


class PostsFeed(Feed):
    """Feed RSS."""

    title = settings.CONFERENCE_TITLE
    link = "/blog/"
    description = _("Web de la %s") % settings.CONFERENCE_TITLE

    def items(self):
        return Post.objects.filter(status=PUBLISHED).order_by("-created")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.outstanding_image:
            return mark_safe(
                '<p class="outstanding-image"><img src="{}" class="img-responsive center-block"></p>{}'.format(
                    item.outstanding_image.url, item.content
                )
            )
        return item.content

    def item_link(self, item):
        """links to the whole blog list as we do not
        have by post view"""
        return reverse("blog:list")


class PostsAtomFeed(PostsFeed):
    """Feed Atom."""

    feed_type = Atom1Feed
