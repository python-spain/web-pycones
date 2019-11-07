# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import csv

from django.http import HttpResponse


def download_approved_speakers(modeladmin, request, queryset):
    """Downloads as a CSV file the list of approved speakers, with name and email."""
    speakers = filter(lambda item: item.is_approved(), queryset)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=speakers.csv"
    writer = csv.writer(response)
    for speaker in speakers:
        writer.writerow([speaker.name, speaker.user.email])
    return response

download_approved_speakers.short_description = "Download approved speakers"
