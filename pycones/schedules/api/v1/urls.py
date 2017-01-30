# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from schedule.api.v1.resources import ScheduleResource


urlpatterns = [
    url(r'schedule/', include(ScheduleResource.urls())),
]
