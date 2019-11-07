# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import override_settings
from django.utils.text import slugify
from test_plus.test import TestCase

from pycones.blog.models import Post
from pycones.blog.tests.factories import PostFactory
from pycones.users.tests.factories import UserFactory


@override_settings(LANDING_GLOBAL_REDIRECT=False)
class PostModelTests(TestCase):

    def test_create_post(self):
        prev_posts = Post.objects.count()
        Post.objects.create(
            author=UserFactory(),
            content="foo",
            title="Title",
            slug="Title"
        )
        self.assertEqual(prev_posts + 1, Post.objects.count())

    def test_create_slug(self):
        post = PostFactory(author=UserFactory())
        post.save()
        self.assertEqual(post.slug, slugify(post.title))

    def test_more(self):
        original_summary = "part1"
        post = Post.objects.create(
            author=UserFactory(),
            content="{}<!--more-->more".format(original_summary),
            title="Title",
            slug="Title"
        )
        summary = post.summary()
        self.assertEqual(summary, '{}<p><a href="/es/blog/title/">Seguir leyendo...</a></p>'.format(original_summary))
