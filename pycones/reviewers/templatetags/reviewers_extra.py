# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django import template
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
