# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from test_plus import TestCase

from pycones.users.forms import SignInForm, RestorePasswordForm, RequestRestoreCodeForm
from pycones.users.tests.factories import UserFactory


class SignInFormTests(TestCase):

    def setUp(self):
        self.password = "pass"
        self.user = UserFactory()
        self.user.set_password(self.password)
        self.user.save()

    def test_sign_in_success(self):
        form = SignInForm({
            "email": self.user.email,
            "password": self.password,
        })
        self.assertTrue(form.is_valid())

    def test_sign_in_error_password(self):
        form = SignInForm({
            "email": self.user.email,
            "password": "error",
        })
        self.assertFalse(form.is_valid())

    def test_sign_in_error_email(self):
        form = SignInForm({
            "email": 'error@example.com',
            "password": self.password,
        })
        self.assertFalse(form.is_valid())


class RestorePasswordFormTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user.generate_restore_code()

    def test_restore_code_success(self):
        form = RestorePasswordForm({
            "email": self.user.email,
            "restore_code": self.user.restore_code,
            "password": "new-password",
            "repeat_password": "new-password",
        })
        self.assertTrue(form.is_valid())


class RequestRestoreCodeFormTests(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_restore_code_success(self):
        form = RequestRestoreCodeForm({
            "email": self.user.email,
        })
        self.assertTrue(form.is_valid())

    def test_restore_code_fails(self):
        form = RequestRestoreCodeForm({
            "email": "bad@example.com",
        })
        self.assertTrue(form.is_valid())
