# -*- coding: utf-8 -*-
from django.contrib import admin
from pycones.jobboard.models import JobOffer
from pycones.utils.actions import export_as_csv_action


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "employer"]
    list_filter = []
    actions = [
        export_as_csv_action(
            "CSV Export", fields=["id", "title", "employer", "description"]
        )
    ]
