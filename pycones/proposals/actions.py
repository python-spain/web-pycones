import csv

from django.http import HttpResponse
from django.utils.encoding import smart_text


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in Django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        if fields:
            fieldset = set(fields)
            field_names = fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = set(fields) - excludeset
        else:
            field_names = set()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=%s.csv" % smart_text(opts).replace(".", "_")
        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow(
                [smart_text(getattr(obj, field)) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


def send_confirmation_action(description="Send confirmation email"):
    def send_confirmation(modeladmin, request, queryset):
        for item in queryset:
            item.notify()
    send_confirmation.short_description = description
    return send_confirmation


def send_acceptance_action(description="Send acceptance email"):
    def send_acceptance(modeladmin, request, queryset):
        for item in queryset:
            item.notify_acceptance()
    send_acceptance.short_description = description
    return send_acceptance
