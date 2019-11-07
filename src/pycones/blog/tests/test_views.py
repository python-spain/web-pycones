# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import override_settings
from test_plus.test import TestCase

from pycones.blog import PUBLISHED
from pycones.blog.models import Post
from pycones.blog.tests.factories import PostFactory
from pycones.users.tests.factories import UserFactory


@override_settings(LANDING_GLOBAL_REDIRECT=False)
class BlogViewTests(TestCase):

    def test_blog(self):
        PostFactory.create_batch(size=5, author=UserFactory())
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)

    def test_blog_feed(self):
        PostFactory.create_batch(size=5, author=UserFactory())
        response = self.client.get(reverse('blog:blog_feed'))
        self.assertEqual(response.status_code, 200)

    def test_blog_atom(self):
        PostFactory.create_batch(size=5, author=UserFactory())
        response = self.client.get(reverse('blog:blog_atom'))
        self.assertEqual(response.status_code, 200)

    def test_blog_details(self):
        post = Post.objects.create(
            author=UserFactory(), title="Title", slug="slug", status=PUBLISHED
        )
        response = self.client.get(reverse('blog:post', kwargs={'slug': post.slug}))
        self.assertEqual(response.status_code, 200)
