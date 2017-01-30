# -*- coding: utf-8 -*-
from django.conf.urls import url

from pycones.speakers.views import EditSpeaker

urlpatterns = [
    url(r'^$', EditSpeaker.as_view(), name="edit"),
]
