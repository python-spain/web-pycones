# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


BASIC_LEVEL, INTERMEDIATE_LEVEL, ADVANCED_LEVEL = "basic", "intermediate", "advanced"

PROPOSAL_LEVELS = (
    (BASIC_LEVEL, _("Básico")),
    (INTERMEDIATE_LEVEL, _("Intermedio")),
    (ADVANCED_LEVEL, _("Avanzado")),
)

PROPOSAL_LANGUAGES = (
    ("es", _("Español")),
    ("en", _("Inglés")),
)

PROPOSAL_DURATIONS = (
    (15, _("15 minutos")),
    (30, _("30 minutos")),
)

default_app_config = 'pycones.proposals.apps.ProposalsConfig'
