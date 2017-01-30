# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.test import override_settings
from django.urls import reverse
from test_plus import TestCase

from pycones.users.tests.factories import UserFactory
from pycones.utils.urls import reload_urlconf


@override_settings(LANDING_GLOBAL_REDIRECT=False)
class SignInViewTests(TestCase):

    def setUp(self):
        reload_urlconf()
        self.password = "password"
        self.user = UserFactory()
        self.user.set_password(self.password)
        self.user.save()

    def _authenticate(self):
        self.client.login(
            email=self.user.email,
            password=self.password,
            is_validate=True,
        )

    def test_show_sign_in_form(self):
        response = self.client.get(reverse('users:sign-in'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_sign_in_form(self):
        self._authenticate()
        response = self.client.get(reverse('users:sign-in'))
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_sign_out(self):
        self._authenticate()
        response = self.client.get(reverse('users:sign-out'))
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_post_sign_in_form(self):
        data = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(reverse('users:sign-in'), data=data)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_post_sign_in_form_bad_password(self):
        data = {
            "email": self.user.email,
            "password": "bad",
        }
        response = self.client.post(reverse('users:sign-in'), data=data)
        self.assertEqual(response.status_code, 200)


@override_settings(LANDING_GLOBAL_REDIRECT=False)
class RequestRestoreCodeViewTests(TestCase):

    def setUp(self):
        reload_urlconf()
        self.user = UserFactory()
        self.user.save()

    def test_get_request_restore_code_form(self):
        response = self.client.get(reverse('users:request-restore-password'))
        self.assertEqual(response.status_code, 200)

    def test_post_request_request_restore_code(self):
        data = {
            "email": self.user.email
        }
        response = self.client.post(reverse('users:request-restore-password'), data=data)
        self.assertEquals(response.status_code, 200)

    def test_post_request_request_restore_code_bad_email(self):
        data = {
            "email": "bad@example.com"
        }
        response = self.client.post(reverse('users:request-restore-password'), data=data)
        self.assertRedirects(response, reverse('users:request-restore-password'), status_code=302, target_status_code=200)


@override_settings(LANDING_GLOBAL_REDIRECT=False)
class RestorePasswordViewTests(TestCase):

    def setUp(self):
        reload_urlconf()
        self.user = UserFactory()
        self.user.generate_restore_code()

    def test_get_restore_password_form(self):
        response = self.client.get(reverse('users:restore-password', kwargs={"restore_code": self.user.restore_code}))
        self.assertEqual(response.status_code, 200)

    def test_post_restore_password_form(self):
        data = {
            "email": self.user.email,
            "restore_code": self.user.restore_code,
            "password": "new-password",
            "repeat_password": "new-password",
        }
        response = self.client.post(
            reverse('users:restore-password', kwargs={"restore_code": self.user.restore_code}),
            data=data
        )
        self.assertRedirects(response, reverse('users:sign-in'), status_code=302, target_status_code=200)

    def test_post_restore_password_form_bad_code(self):
        data = {
            "email": self.user.email,
            "restore_code": "bad",
            "password": "new-password",
            "repeat_password": "new-password",
        }
        response = self.client.post(
            reverse('users:restore-password', kwargs={"restore_code": self.user.restore_code}),
            data=data
        )
        self.assertEqual(response.status_code, 200)

    def test_post_restore_password_form_bad_password(self):
        data = {
            "email": self.user.email,
            "restore_code": self.user.restore_code,
            "password": "new-password",
            "repeat_password": "new-passwrd",
        }
        response = self.client.post(
            reverse('users:restore-password', kwargs={"restore_code": self.user.restore_code}),
            data=data
        )
        self.assertEqual(response.status_code, 200)

    def test_post_restore_password_form_bad_email(self):
        data = {
            "email": "bad@example.com",
            "restore_code": self.user.restore_code,
            "password": "new-password",
            "repeat_password": "new-password",
        }
        response = self.client.post(
            reverse('users:restore-password', kwargs={"restore_code": self.user.restore_code}),
            data=data
        )
        self.assertEqual(response.status_code, 200)

