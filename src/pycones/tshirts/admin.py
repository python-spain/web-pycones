#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from pycones.tshirts.models import TshirtBooking


class TshirtBookingResource(resources.ModelResource):

    class Meta:
        model = TshirtBooking


@admin.register(TshirtBooking)
class TshirtBookingExportAdmin(ImportExportModelAdmin):
    resource_class = TshirtBookingResource

    list_display = ('email', 'booking_id', 'tshirt_size', 'sex', 'nif', 'date_sent', )
    list_editable = ('tshirt_size', 'sex', )
    readonly_fields = ('date_sent', )

    list_filter = ('date_sent', 'tshirt_size', 'sex', )
    search_fields = ('email', 'booking_id', 'nif', )

    fieldsets = (
        (_('Asistente'), {
            'fields': ('email', 'booking_id', 'nif'),
        }),
        (_('Camisa'), {
            'fields': (('tshirt_size', 'sex', ), ),
        }),
        (_('Otros'), {
            'fields': ('date_sent', ),
        }),
    )
