# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from pycones.configurations.models import Option


def options(request):
    """Context processor that adds options to the template context."""
    return {option.name: option.get_value() for option in Option.objects.all()}
