import csv

from django.http import HttpResponse
from django.utils.encoding import smart_text


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
