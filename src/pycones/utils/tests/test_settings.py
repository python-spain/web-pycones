# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.test import override_settings
from django.urls import NoReverseMatch
from django.urls import reverse
from test_plus.test import TestCase

from pycones.utils.urls import reload_urlconf


class TestSettings(TestCase):

    @override_settings(LANDING_GLOBAL_REDIRECT=True)
    def test_landing_global_redirect(self):
        reload_urlconf()
        with self.assertRaises(NoReverseMatch):
            reverse("info")
            reverse("blog:list")
        response = self.client.get('/admin/login/')
        self.assertEquals(response.status_code, 200)
