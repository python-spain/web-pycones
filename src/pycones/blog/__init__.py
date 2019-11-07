# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


DRAFT, SCHEDULED, PUBLISHED = (0, 1, 2)
STATUSES = (
    (DRAFT, _("Draft")),
    (SCHEDULED, _("Scheduled")),
    (PUBLISHED, _("Published")),
)
