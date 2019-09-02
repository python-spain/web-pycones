from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from pycones.tshirts.models import TshirtBooking


class TshirtBookingResource(resources.ModelResource):

    class Meta:
        model = TshirtBooking


class TshirtBookingExportAdmin(ImportExportModelAdmin):
    resource_class = TshirtBookingResource


admin.site.register(TshirtBooking, TshirtBookingExportAdmin)



