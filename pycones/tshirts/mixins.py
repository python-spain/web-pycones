#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.http import Http404
from options.models import Option


class DisabledByOptionViewMixin:
    """
    Checks on the options package if the given page is disabled.
    Raises a 404 if it is.

    Options package:
    https://github.com/marcosgabarda/django-simple-options
    """
    disabled_option = 'tshirts_page_activated'

    def get_disabled_option(self):
        return self.disabled_option

    def dispatch(self, request, *args, **kwargs):
        """ Raises a 404 if the page marked as disabled. """

        # Check if the page is enabled (staff can skip this), defaults to False
        if not Option.objects.get_value(self.get_disabled_option(), 0) and not self.request.user.is_staff:
            raise Http404

        # Not disabled, proceed with super
        return super().dispatch(request, *args, **kwargs)
