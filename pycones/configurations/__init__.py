# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


FLOAT, INT, STRING = (0, 1, 2)
TYPE_CHOICES = (
    (FLOAT, _("Float")),
    (INT, _("Integer")),
    (STRING, _("String")),
)

DEFAULT_OPTIONS = {
    "submit_proposal_opened": {
        "value": 0,
        "type": INT,
        "public_name": "Set the submit of proposals opened"
    },
    "schedule_opened": {
        "value": 0,
        "type": INT,
        "public_name": "Makes the schedule visible"
    },
    "attendees_zone_activated": {
        "value": 0,
        "type": INT,
        "public_name": "Activates the attendees zone"
    },
    "activated_tickets_sale_button": {
        "value": 0,
        "type": INT,
        "public_name": "Activates button for selling tickets"
    },
    "activated_tickets_sale_page": {
        "value": 0,
        "type": INT,
        "public_name": "Activates page for selling tickets"
    },
    "sold_out": {
        "value": 0,
        "type": INT,
        "public_name": "Sets tickets as sold out"
    },
}

default_app_config = 'pycones.configurations.apps.ConfigurationsConfig'
