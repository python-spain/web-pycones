# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from xml.etree import ElementTree

import math

from icalendar import Calendar, Event


def export_to_pentabarf(schedule):
    """Export schedule model to Pentabarf XML format.
    :param schedule:
    """
    schedule_root = ElementTree.Element('schedule')

    # Conference
    conference_element = ElementTree.SubElement(schedule_root, 'conference')
    title = ElementTree.SubElement(conference_element, 'title')
    title.text = "PyConES 2016"
    ElementTree.SubElement(conference_element, 'subtitle')
    venue = ElementTree.SubElement(conference_element, 'venue')
    venue.text = "Universidad de Almería"
    start = ElementTree.SubElement(conference_element, 'start')
    start.text = "2016-10-07"
    end = ElementTree.SubElement(conference_element, 'end')
    end.text = "2016-10-09"
    days = ElementTree.SubElement(conference_element, 'days')
    days.text = str(schedule.day_set.count())
    timeslot_duration = ElementTree.SubElement(conference_element, 'timeslot_duration')
    timeslot_duration.text = "00:40"

    # Days
    for index, day in enumerate(schedule.day_set.all()):
        day_element = ElementTree.SubElement(
            schedule_root, 'day', attrib={"date": day.date.strftime("%Y-%m-%d"), "index": str(index + 1)}
        )

        # Rooms
        rooms = dict()
        for room in schedule.room_set.all():
            room_element = ElementTree.SubElement(
                day_element, 'room', attrib={"name": room.name}
            )
            rooms[room.pk] = room_element

        # Slots
        for slot in day.slot_set.order_by("start"):
            if slot.kind.plenary:
                room_element = rooms[slot.default_room.pk]
                event_element = ElementTree.SubElement(room_element, 'event', attrib={"id": str(slot.pk)})
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
                duration = datetime.datetime.combine(datetime.date.today(), slot.end) - \
                    datetime.datetime.combine(datetime.date.today(), slot.start)
                duration_element.text = "{:02}:{:02}".format(
                    math.floor(duration.seconds/60/60),
                    math.floor((duration.seconds/60) % 60)
                )
                room_name_element = ElementTree.SubElement(event_element, "room")
                room_name_element.text = slot.default_room.name
                title_element = ElementTree.SubElement(event_element, "title")
                title_element.text = slot.content_override.raw
            if slot.content is not None and slot.default_room is not None:
                room_element = rooms[slot.default_room.pk]
                event_element = ElementTree.SubElement(room_element, 'event', attrib={"id": str(slot.pk)})
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
                duration = datetime.datetime.combine(datetime.date.today(), slot.end) - \
                    datetime.datetime.combine(datetime.date.today(), slot.start)
                duration_element.text = "{:02}:{:02}".format(
                    math.floor(duration.seconds/60/60),
                    math.floor((duration.seconds/60) % 60)
                )
                room_name_element = ElementTree.SubElement(event_element, "room")
                room_name_element.text = slot.default_room.name
                title_element = ElementTree.SubElement(event_element, "title")
                title_element.text = slot.content.get_title()
                description_element = ElementTree.SubElement(event_element, "description")
                description = slot.content.get_description()
                description_element.text = (description.raw if hasattr(description, "raw") else description).replace("\r\n", "")
                abstract_element = ElementTree.SubElement(event_element, "abstract")
                abstract = slot.content.get_abstract()
                abstract_element.text = (abstract.raw if hasattr(abstract, "raw") else abstract).replace("\r\n", "")
                persons_element = ElementTree.SubElement(event_element, "persons")
                person = slot.content.speaker
                if len(person.name.split(" y ")) > 0:
                    persons = person.name.split(" y ")
                elif len(person.name.split(", ")) > 0:
                    persons = person.name.split(", ")
                else:
                    persons = [person]
                for person in persons:
                    person_element = ElementTree.SubElement(persons_element, "person")
                    person_element.text = person
    return ElementTree.tostring(schedule_root, encoding="unicode")


def export_to_xcal(schedule):
    """Export schedule model to xCal format.
    :param schedule:
    """
    icalendar_root = ElementTree.Element('icalendar', attrib={"xmlns": "urn:ietf:params:xml:ns:icalendar-2.0"})
    vcalendar_element = ElementTree.SubElement(icalendar_root, "vcalendar")
    for index, day in enumerate(schedule.day_set.all()):
        for slot in day.slot_set.all().select_related():
            if slot.kind.plenary:
                vevent_element = ElementTree.SubElement(vcalendar_element, "vevent")
                properties_element = ElementTree.SubElement(vevent_element, "properties")
                summary_element = ElementTree.SubElement(properties_element, "summary")
                text_element = ElementTree.SubElement(summary_element, "text")
                text_element.text = slot.content_override.raw
                location_element = ElementTree.SubElement(properties_element, "location")
                location_element.text = slot.default_room.name
                dtstart_element = ElementTree.SubElement(properties_element, "dtstart")
                date_time_element = ElementTree.SubElement(dtstart_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"),
                    slot.start.strftime("%H:%M:%S"),
                )
                dtend_element = ElementTree.SubElement(properties_element, "dtend")
                date_time_element = ElementTree.SubElement(dtend_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"),
                    slot.end.strftime("%H:%M:%S"),
                )
            if slot.content is not None:
                vevent_element = ElementTree.SubElement(vcalendar_element, "vevent")
                properties_element = ElementTree.SubElement(vevent_element, "properties")
                summary_element = ElementTree.SubElement(properties_element, "summary")
                text_element = ElementTree.SubElement(summary_element, "text")
                text_element.text = slot.content.get_title()
                description = slot.content.get_description()
                description_element = ElementTree.SubElement(properties_element, "description")
                text_element = ElementTree.SubElement(description_element, "text")
                text_element.text = (description.raw if hasattr(description, "raw") else description).replace("\r\n", "")
                location_element = ElementTree.SubElement(properties_element, "location")
                location_element.text = slot.default_room.name
                dtstart_element = ElementTree.SubElement(properties_element, "dtstart")
                date_time_element = ElementTree.SubElement(dtstart_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"),
                    slot.start.strftime("%H:%M:%S"),
                )
                dtend_element = ElementTree.SubElement(properties_element, "dtend")
                date_time_element = ElementTree.SubElement(dtend_element, "date-time")
                date_time_element.text = "{}T{}".format(
                    day.date.strftime("%Y-%m-%d"),
                    slot.end.strftime("%H:%M:%S"),
                )

    return ElementTree.tostring(icalendar_root, encoding="unicode")


def export_to_icalendar(schedule):
    """Export schedule model to iCalendar format.
    :param schedule:
    """
    cal = Calendar()
    for index, day in enumerate(schedule.day_set.all()):
        for slot in day.slot_set.all().select_related():
            if slot.kind.plenary:
                event = Event()
                event['uid'] = slot.pk
                event['dtstart'] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"),
                    slot.start.strftime("%H%M%S"),
                )
                event['dtend'] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"),
                    slot.end.strftime("%H%M%S"),
                )
                if slot.default_room:
                    event.add('location', slot.default_room.name)
                event.add('summary', slot.content_override.raw)
                cal.add_component(event)
            if slot.content is not None:
                event = Event()
                event['uid'] = slot.pk
                event['dtstart'] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"),
                    slot.start.strftime("%H%M%S"),
                )
                event['dtend'] = "{}T{}".format(
                    day.date.strftime("%Y%m%d"),
                    slot.end.strftime("%H%M%S"),
                )
                if slot.default_room:
                    event.add('location', slot.default_room.name)
                event.add('summary', slot.content.get_title())
                description = slot.content.get_description()
                event.add('description', (description.raw if hasattr(description, "raw") else description).replace("\r\n", ""))
                cal.add_component(event)
    return cal.to_ical()

