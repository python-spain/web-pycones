# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


BENEFIT_TEXT, BENEFIT_FILE, BENEFIT_WEB_LOGO, BENEFIT_SIMPLE = "text", "file", "web_logo", "simple"

BENEFIT_TYPE_CHOICES = [
    (BENEFIT_TEXT, _("Text")),
    (BENEFIT_FILE, _("File")),
    (BENEFIT_WEB_LOGO, _("Web Logo")),
    (BENEFIT_SIMPLE, _("Simple"))
]

default_app_config = 'pycones.sponsorships.apps.SponsorshipConfig'
