# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bleach
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from pycones.schedules.helpers import (
    export_to_pentabarf,
    export_to_xcal,
    export_to_icalendar,
    check_schedule_view,
)
from pycones.schedules.models import Slot, Day, Room


class ShowSchedule(View):
    """Shows the schedule of the event."""

    template_name = "schedule/show.html"

    def get(self, request):
        check_schedule_view(request)
        data = {"days": []}
        for day in Day.objects.all():

            data["days"].append(
                {
                    "date": day.date,
                    "slot_groups": day.slot_groups(),
                    "tracks": day.tracks(),
                }
            )
        return render(request, self.template_name, data)


class ShowSlot(View):
    template_name = "schedule/details.html"

    def get(self, request, slot):
        check_schedule_view(request)
        try:
            slot_id = int(slot)
            slot = get_object_or_404(Slot, pk=slot_id)
            if slot.presentation.slug:
                return redirect(slot.get_absolute_url(), permanent=True)
        except ValueError:
            slot = get_object_or_404(Slot, presentation__slug=slot)
        data = {
            "slot": slot,
            "biographies": [
                mark_safe(bleach.clean(speaker.biography.rendered, "script"))
                for speaker in slot.content.get_speakers()
            ],
        }
        return render(request, self.template_name, data)


def pentabarf_view(request):
    """Download Pentabarf calendar file.
    :param request:
    """
    check_schedule_view(request)
    days = Day.objects.all()
    rooms = Room.objects.all()
    pentabarf_xml = export_to_pentabarf(days, rooms)
    return HttpResponse(pentabarf_xml, content_type="application/xml")


def xcal_view(request):
    """Download xCal file.
    :param request:
    """
    check_schedule_view(request)
    days = Day.objects.all()
    xcal_xml = export_to_xcal(days)
    return HttpResponse(xcal_xml, content_type="application/xml")


def icalendar_view(request):
    """Download iCalendar file.
    :param request:
    """
    check_schedule_view(request)
    days = Day.objects.all()
    calendar_text = export_to_icalendar(days)
    return HttpResponse(calendar_text, content_type="text/calendar")
