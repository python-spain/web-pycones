# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.conf.urls import url
from django.template.defaultfilters import date
from restless.dj import DjangoResource
from restless.exceptions import NotFound

from pycones.schedules.models import Schedule, Presentation


class ScheduleResource(DjangoResource):

    @classmethod
    def urls(cls, name_prefix=None):
        return [
            url(r'^$', cls.as_detail(), name=cls.build_url_name('detail', name_prefix)),
        ]

    def detail(self, *args, **kwargs):
        schedule = Schedule.objects.filter(published=True, hidden=False).first()
        if not schedule:
            raise NotFound()

        # Get speakers list
        presentations = Presentation.objects.all()
        speakers = []
        for presentation in presentations:
            speaker = {
                "id": presentation.speaker.get_api_id(),
                "name": presentation.speaker.name,
                "title": "",
                "photo": "",
                "description": presentation.speaker.biography.raw,
                "twitter": "",
            }
            speakers.append(speaker)

        # Get agenda, iterating by day
        agenda = OrderedDict()
        days = schedule.day_set.all()
        for day in days:
            tracks = list(day.track_set.all())
            day_name = date(day.date, "l d F Y")
            for slots in day.slot_groups():
                for slot_index, slot in enumerate(slots):
                    try:
                        track = tracks[slot_index]
                    except IndexError:
                        track = tracks[0]
                    talk = None
                    if slot.content:
                        talk = {
                            "id": slot.content.get_api_id(),
                            "name": slot.content.get_title(),
                            "hour": date(slot.start, "H:i"),
                            "duration": slot.content.proposal.duration,
                            "speakers": [slot.content.speaker.get_api_id()]
                        }
                    if track.name not in agenda:
                        agenda[track.name] = {
                            "name": track.name,
                            "place": "",
                            "days": dict()
                        }
                    if talk:
                        if day_name not in agenda[track.name]["days"]:
                            agenda[track.name]["days"][day_name] = {
                                "name": day_name,
                                "talks": []
                            }
                        agenda[track.name]["days"][day_name]["talks"].append(talk)
        for key, value in agenda.items():
            agenda[key]["days"] = list(agenda[key]["days"].values())
        agenda = list(agenda.values())
        return {
            "id": "PyConES16",
            "name": "PyConES 2016 Almería",
            "shortname": "PyConES 2016",
            "date": "07/10/2016",
            "place": "Almería",
            "logo": "http://2016.es.pycon.org/static/img/logo2016.jpg",
            "location": {
                "img": "http://maps.googleapis.com/maps/api/staticmap?center=36.8293266,-2.4066496&zoom=15&"
                       "scale=false&size=600x300&maptype=roadmap&format=png&visual_refresh=true&"
                       "markers=size:mid%7Ccolor:0xff0000%7Clabel:%7C36.8293266,-2.4066496",
                "text": "Universidad de Almería, Ctra. Sacramento, s/n, 04120 La Cañada de San Urbano, Almería"
            },
            "agenda": agenda,
            "speakers": speakers,
        }
