# -*- coding: utf-8 -*-
import datetime
from xml.etree import ElementTree

import math

from django.http import Http404
from icalendar import Calendar, Event
from options.models import Option


def check_schedule_view(request):
    is_schedule_opened = Option.objects.get_value("schedule_opened", 0) != 0
    if not is_schedule_opened and not (
        request.user.is_authenticated and request.user.is_superuser
    ):
        raise Http404()


def export_to_pentabarf(days_queryset, rooms_queryset):
    """Export schedule model to Pentabarf XML format.
    :param days_queryset:
    :param rooms_queryset:
    """
    schedule_root = ElementTree.Element("schedule")

    # Conference
    conference_element = ElementTree.SubElement(schedule_root, "conference")
    title = ElementTree.SubElement(conference_element, "title")
    title.text = "PyConES 2019"
    ElementTree.SubElement(conference_element, "subtitle")
    venue = ElementTree.SubElement(conference_element, "venue")
    venue.text = "Alicante"
    start = ElementTree.SubElement(conference_element, "start")
    start.text = "2019-10-4"
    end = ElementTree.SubElement(conference_element, "end")
    end.text = "2019-10-6"
    days = ElementTree.SubElement(conference_element, "days")
    days.text = str(days_queryset.count())
    timeslot_duration = ElementTree.SubElement(conference_element, "timeslot_duration")
    timeslot_duration.text = "00:20"

    # Days
    for index, day in enumerate(days_queryset.all()):
        day_element = ElementTree.SubElement(
            schedule_root,
            "day",
            attrib={"date": day.date.strftime("%Y-%m-%d"), "index": str(index + 1)},
        )

        # Rooms
        rooms = dict()
        for room in rooms_queryset.all():
            room_element = ElementTree.SubElement(
                day_element, "room", attrib={"name": room.name}
            )
            rooms[room.pk] = room_element

        # Slots
        for slot in day.slot_set.order_by("start"):
            if slot.kind.plenary:
                if slot.room is not None:
                    room_element = rooms[slot.room.pk]
                else:
                    continue
                event_element = ElementTree.SubElement(
                    room_element, "event", attrib={"id": str(slot.pk)}
                )
                date_element = ElementTree.SubElement(event_element, "date")
                date_element.text = datetime.datetime(
                    day=slot.day.date.day,
                    month=slot.day.date.month,
                    year=slot.day.date.year,
                    hour=slot.start.hour,
                    minute=slot.start.minute,
                ).strftime("%Y-%m-%dT%H:%M:%S+0100")
                start_element = ElementTree.SubElement(event_element, "start")
                start_element.text = slot.start.strftime("%H:%M")
                duration_element = ElementTree.SubElement(event_element, "duration")
                duration = datetime.datetime.combine(
                    datetime.date.today(), slot.end
                ) - datetime.datetime.combine(datetime.date.today(), slot.start)
                duration_element.text = "{:02}:{:02}".format(
                    math.floor(duration.seconds / 60 / 60),
                    math.floor((duration.seconds / 60) % 60),
                )
                room_name_element = ElementTree.SubElement(event_element, "room")
                room_name_element.text = slot.room.name
                title_element = ElementTree.SubElement(event_element, "title")
                title_element.text = slot.content_override.raw
            if slot.content is not None and slot.room is not None:
                room_element = rooms[slot.room.pk]
                event_element = ElementTree.SubElement(
                    room_element, "event", attrib={"id": str(slot.pk)}
                )
                date_element = ElementTree.SubElement(event_element, "date")
                date_element.text = datetime.datetime(
                    day=slot.day.date.day,
                    month=slot.day.date.month,
                    year=slot.day.date.year,
                    hour=slot.start.hour,
                    minute=slot.start.minute,
                ).strftime("%Y-%m-%dT%H:%M:%S+0100")
                start_element = ElementTree.SubElement(event_element, "start")
                start_element.text = slot.start.strftime("%H:%M")
                duration_element = ElementTree.SubElement(event_element, "duration")
                duration = datetime.datetime.combine(
                    datetime.date.today(), slot.end
                ) - datetime.datetime.combine(datetime.date.today(), slot.start)
                duration_element.text = "{:02}:{:02}".format(
                    math.floor(duration.seconds / 60 / 60),
                    math.floor((duration.seconds / 60) % 60),
                )
                room_name_element = ElementTree.SubElement(event_element, "room")
                room_name_element.text = slot.room.name
                title_element = ElementTree.SubElement(event_element, "title")
                title_element.text = slot.title
                description = slot.description
                if description:
                    description_element = ElementTree.SubElement(
                        event_element, "description"
                    )
                    description_element.text = (
                        description.raw if hasattr(description, "raw") else description
                    ).replace("\r\n", "")
                abstract = slot.content.get_abstract()
                if abstract:
                    abstract_element = ElementTree.SubElement(event_element, "abstract")
                    abstract_element.text = (
                        abstract.raw if hasattr(abstract, "raw") else abstract
                    ).replace("\r\n", "")
                person = slot.content.speakers.first()
                if person:
                    persons_element = ElementTree.SubElement(event_element, "persons")
                    if len(person.name.split(" y ")) > 0:
                        persons = person.name.split(" y ")
                    elif len(person.name.split(", ")) > 0:
                        persons = person.name.split(", ")
                    else:
                        persons = [person]
                    for person in persons:
                        person_element = ElementTree.SubElement(
                            persons_element, "person"
                        )
                        person_element.text = person
    return ElementTree.tostring(schedule_root, encoding="unicode")


def export_to_xcal(days_queryset):
    """Export schedule model to xCal format.
    :param days_queryset:
    """
    icalendar_root = ElementTree.Element(
        "icalendar", attrib={"xmlns": "urn:ietf:params:xml:ns:icalendar-2.0"}
    )
    vcalendar_element = ElementTree.SubElement(icalendar_root, "vcalendar")
    for index, day in enumerate(days_queryset.all()):
        for slot in day.slot_set.all().select_related():
            if slot.kind.plenary:
                vevent_element = ElementTree.SubElement(vcalendar_element, "vevent")
                properties_element = ElementTree.SubElement(
                    vevent_element, "properties"
                )
                summary_element = ElementTree.SubElement(properties_element, "summary")
                text_element = ElementTree.SubElement(summary_element, "text")
                text_element.text = slot.content_override.raw
                location_element = ElementTree.SubElement(
                    properties_element, "location"
                )
                location_element.text = slot.room.name if slot.room is not None else ""
                dtstart_element = ElementTree.SubElement(properties_element, "dtstart")
                date_time_element = ElementTree.SubElement(dtstart_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"), slot.start.strftime("%H:%M:%S")
                )
                dtend_element = ElementTree.SubElement(properties_element, "dtend")
                date_time_element = ElementTree.SubElement(dtend_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"), slot.end.strftime("%H:%M:%S")
                )
            if slot.content is not None:
                vevent_element = ElementTree.SubElement(vcalendar_element, "vevent")
                properties_element = ElementTree.SubElement(
                    vevent_element, "properties"
                )
                summary_element = ElementTree.SubElement(properties_element, "summary")
                text_element = ElementTree.SubElement(summary_element, "text")
                text_element.text = slot.title
                description = slot.description
                description_element = ElementTree.SubElement(
                    properties_element, "description"
                )
                if description:
                    text_element = ElementTree.SubElement(description_element, "text")
                    text_element.text = (
                        description.raw if hasattr(description, "raw") else description
                    ).replace("\r\n", "")
                location_element = ElementTree.SubElement(
                    properties_element, "location"
                )
                location_element.text = slot.room.name
                dtstart_element = ElementTree.SubElement(properties_element, "dtstart")
                date_time_element = ElementTree.SubElement(dtstart_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"), slot.start.strftime("%H:%M:%S")
                )
                dtend_element = ElementTree.SubElement(properties_element, "dtend")
                date_time_element = ElementTree.SubElement(dtend_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"), slot.end.strftime("%H:%M:%S")
                )

    return ElementTree.tostring(icalendar_root, encoding="unicode")


def export_to_icalendar(days_queryset):
    """Export schedule model to iCalendar format.
    :param days_queryset:
    """
    cal = Calendar()
    for index, day in enumerate(days_queryset.all()):
        for slot in day.slot_set.all().select_related():
            if slot.kind.plenary:
                event = Event()
                event["uid"] = slot.pk
                event["dtstart"] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"), slot.start.strftime("%H%M%S")
                )
                event["dtend"] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"), slot.end.strftime("%H%M%S")
                )
                if slot.room:
                    event.add("location", slot.room.name)
                event.add("summary", slot.content_override.raw)
                cal.add_component(event)
            if slot.content is not None:
                event = Event()
                event["uid"] = slot.pk
                event["dtstart"] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"), slot.start.strftime("%H%M%S")
                )
                event["dtend"] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"), slot.end.strftime("%H%M%S")
                )
                if slot.room:
                    event.add("location", slot.room.name)
                event.add("summary", slot.title)
                description = slot.description
                if description:
                    event.add(
                        "description",
                        (
                            description.raw
                            if hasattr(description, "raw")
                            else description
                        ).replace("\r\n", ""),
                    )
                cal.add_component(event)
    return cal.to_ical()

