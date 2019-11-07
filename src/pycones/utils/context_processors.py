# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf import settings


def project_settings(request):
    """Context processor that adds options to the template context."""
    variables = ["CONFERENCE_TITLE", "LANDING_GLOBAL_REDIRECT", "CONTACT_EMAIL", "SPONSORS_EMAIL",
                 "CFP_EMAIL", "PRESS_EMAIL"]
    return {variable: getattr(settings, variable) for variable in variables}
