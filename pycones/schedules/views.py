# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bleach
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from options.models import Option

from pycones.schedules.forms import PresentationForm
from pycones.schedules.helpers import export_to_pentabarf, export_to_xcal, export_to_icalendar
from pycones.schedules.models import Schedule, Slot, Presentation


def check_schedule_view(request):
    is_schedule_opened = bool(Option.objects.get_value("schedule_opened", 0))
    if not is_schedule_opened and not (request.user.is_authenticated() and request.user.is_superuser):
        raise Http404()


class ShowSchedule(View):
    """Shows the schedule of the event."""
    template_name = "schedule/show.html"

    def get(self, request):
        check_schedule_view(request)
        schedule = Schedule.objects.filter(published=True, hidden=False).first()
        if not schedule:
            raise Http404()
        data = {"days": []}
        for day in schedule.day_set.all():
            data["days"].append({
                "tracks": day.track_set.order_by("order"),
                "date": day.date,
                "slots": day.slot_set.all().select_related(),
                "slot_groups": day.slot_groups(),
            })
        return render(request, self.template_name, data)


class ShowSlot(View):
    template_name = "schedule/details.html"

    def get(self, request, slot):
        check_schedule_view(request)
        try:
            slot_id = int(slot)
            slot = get_object_or_404(Slot, pk=slot_id)
            if slot.content_ptr.slug:
                return redirect(slot.get_absolute_url(), permanent=True)
        except ValueError:
            slot = get_object_or_404(Slot, content_ptr__slug=slot)
        data = {
            "slot": slot,
            "biography": mark_safe(bleach.clean(slot.content.speaker.biography.rendered, 'script'))
        }
        return render(request, self.template_name, data)


class EditPresentation(LoginRequiredMixin, View):
    template_name = "schedule/presentations/edit.html"

    def get_login_url(self):
        return reverse("speakers:sign-in")

    def get(self, request, presentation_id):
        presentation = get_object_or_404(Presentation, pk=presentation_id, speaker=request.user.speaker_profile)
        form = PresentationForm(instance=presentation)
        data = {
            "presentation": presentation,
            "form": form
        }
        return render(request, self.template_name, data)

    def post(self, request, presentation_id):
        presentation = get_object_or_404(Presentation, pk=presentation_id, speaker=request.user.speaker_profile)
        form = PresentationForm(request.POST, request.FILES, instance=presentation)
        data = {
            "presentation": presentation,
            "form": form
        }
        if form.is_valid():
            form.save()
            messages.success(request, _("Datos actualizados correctamente"))
            return redirect(reverse("speakers:edit"))
        return render(request, self.template_name, data)


def pentabarf_view(request):
    """Download Pentabarf calendar file.
    :param request:
    """
    check_schedule_view(request)
    schedule = Schedule.objects.filter(published=True, hidden=False).first()
    pentabarf_xml = export_to_pentabarf(schedule)
    return HttpResponse(pentabarf_xml, content_type="application/xml")


def xcal_view(request):
    """Download xCal file.
    :param request:
    """
    check_schedule_view(request)
    schedule = Schedule.objects.filter(published=True, hidden=False).first()
    xcal_xml = export_to_xcal(schedule)
    return HttpResponse(xcal_xml, content_type="application/xml")


def icalendar_view(request):
    """Download iCalendar file.
    :param request:
    """
    check_schedule_view(request)
    schedule = Schedule.objects.filter(published=True, hidden=False).first()
    calendar_text = export_to_icalendar(schedule)
    return HttpResponse(calendar_text, content_type="text/calendar")
