# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from pycones.sponsorships.models import BenefitLevel, SponsorLevel, Sponsor, Benefit
from pycones.sponsorships.models import SponsorBenefit


class BenefitLevelInline(admin.TabularInline):
    model = BenefitLevel
    extra = 0


class SponsorBenefitInline(admin.StackedInline):
    model = SponsorBenefit
    extra = 0
    fieldsets = [
        (None, {
            "fields": [
                ("benefit", "active"),
                ("max_words", "other_limits"),
                "text",
                "upload",
            ]
        })
    ]


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = [
        (None, {
            "fields": [
                ("name", "applicant"),
                ("level", "active"),
                "external_url",
                "annotation",
                ("contact_name", "contact_email")
            ]
        }),
        ("Metadata", {
            "fields": ["added"],
            "classes": ["collapse"]
        })
    ]
    inlines = [SponsorBenefitInline]
    list_display = ["name", "external_url", "level", "active"]

    def get_form(self, *args, **kwargs):
        # @@@ kinda ugly but using choices= on NullBooleanField is broken
        form = super(SponsorAdmin, self).get_form(*args, **kwargs)
        form.base_fields["active"].widget.choices = [
            ("1", "unreviewed"),
            ("2", "approved"),
            ("3", "rejected")
        ]
        return form


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "description"]
    inlines = [BenefitLevelInline]


@admin.register(SponsorLevel)
class SponsorLevelAdmin(admin.ModelAdmin):
    inlines = [BenefitLevelInline]
