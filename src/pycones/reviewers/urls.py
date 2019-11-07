# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

from pycones.reviewers.views import ReviewerSignUpView, ReviewView, ReviewListView

app_name = "reviewers"

urlpatterns = [
    url(
        r"^sign-up/success/$",
        TemplateView.as_view(template_name="reviewers/sign_up_success.html"),
        name="sign-up-success",
    ),
    url(r"^sign-up/$", ReviewerSignUpView.as_view(), name="sign-up"),
    url(r"^(?P<pk>\d+)/$", ReviewView.as_view(), name="details"),
    url(r"^$", ReviewListView.as_view(), name="list"),
]
