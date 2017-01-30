# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.conf.urls import url

from pycones.users.views import SignInView, RequestRestorePasswordView, RestorePasswordView, SignOutView

urlpatterns = [
    url(r'^sign-out/$', SignOutView.as_view(), name="sign-out"),
    url(r'^sign-in/$', SignInView.as_view(), name="sign-in"),
    url(r'^request-restore-password/$', RequestRestorePasswordView.as_view(), name="request-restore-password"),
    url(r'^restore-password/(?P<restore_code>.+)/$', RestorePasswordView.as_view(), name="restore-password"),
]
