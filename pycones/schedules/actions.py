# -*- coding: utf-8 -*-
import csv

from django.http import HttpResponse


def download_speakers(modeladmin, request, queryset):
    """Downloads as a CSV file the list of approved speakers, with name and email."""
    speakers = []
    for presentation in queryset:
        speakers += list(presentation.get_speakers())
    speakers = set(speakers)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=speakers.csv"
    writer = csv.writer(response)
    for speaker in speakers:
        writer.writerow([speaker.name, speaker.user.email])
    return response


download_speakers.short_description = "Download speakers"


def create_slots(modeladmin, request, queryset):
    origin = queryset.first()
    for t in origin.day.tracks():
        if origin.track == t:
            continue
        origin.id = None
        origin.track = t
        origin.save()
