# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pycones.reviewers.forms import ReviewAdminForm
from pycones.reviewers.models import Review, Reviewer
from .actions import export_as_csv_action


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "proposal", "user", "relevance", "interest", "newness", "get_avg", "conflict", "finished",
                    "created"]
    list_filter = ["proposal", "user", "conflict", "finished"]

    actions = [
        export_as_csv_action("CSV Export", fields=[
            "id",
            "proposal",
            "user",
            "relevance",
            "interest",
            "newness",
            "avg_property",
            "conflict",
            "finished",
            "created",
        ])
    ]

    form = ReviewAdminForm

    def get_avg(self, instance):
        return instance.avg()
    get_avg.short_description = _("Media")


@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "get_reviews", "created"]

    def get_reviews(self, instance):
        return instance.reviews_count()
    get_reviews.short_description = _("Revisiones")
