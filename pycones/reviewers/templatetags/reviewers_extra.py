# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def iconic(value):
    if isinstance(value, bool):
        if value:
            return mark_safe('<span class="label label-pill label-success">'
                             '<i class="fa fa-check" aria-hidden="true"></i>'
                             '</span>')
        return mark_safe('<span class="label label-pill label-danger">'
                         '<i class="fa fa-times" aria-hidden="true"></i>'
                         '</span>')
    return value


@register.filter
def is_reviewer(user):
    """Checks if the user is a reviewer."""
    if user.is_superuser:
        return True
    if user.is_authenticated:
        try:
            _ = user.reviewer
        except ObjectDoesNotExist:
            return False
        return True
    return False
