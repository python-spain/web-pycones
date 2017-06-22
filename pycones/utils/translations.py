# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.conf import settings
from markupfield.fields import Markup


def get_translated_markdown_field(model, field_name):
    """Fixes the problem this Markup fields with translations."""
    field = getattr(model, field_name)
    assert isinstance(field, Markup)
    if not field.raw:
        for language in settings.MODELTRANSLATION_FALLBACK_LANGUAGES:
            translated_field = getattr(model, "%s_%s" % (field_name, language))
            if translated_field.raw:
                return translated_field
    return field

