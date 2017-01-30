# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import SET_NULL
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField

from pycones.proposals.models import Proposal


@python_2_unicode_compatible
class Schedule(models.Model):

    published = models.BooleanField(default=True)
    hidden = models.BooleanField("Hide schedule from overall conference view", default=False)

    class Meta:
        ordering = ["section"]

    def __str__(self):
        return "%s Schedule" % self.section


@python_2_unicode_compatible
class Day(models.Model):

    schedule = models.ForeignKey(Schedule)
    date = models.DateField()

    def __str__(self):
        return "%s" % self.date

    class Meta:
        unique_together = [("schedule", "date")]
        ordering = ["date"]

    def slot_groups(self):
        """Returns all the groups of slots, grouped by start and end hours."""
        groups = OrderedDict()
        for slot in self.slot_set.all().select_related():
            key = "{}-{}".format(slot.start, slot.end)
            try:
                groups[key].append(slot)
            except KeyError:
                groups[key] = [slot]
        values = groups.values()
        ordered_values = []
        for value in values:
            ordered_values.append(sorted(value, key=lambda item: item.order))
        return ordered_values


@python_2_unicode_compatible
class Room(models.Model):

    schedule = models.ForeignKey(Schedule)
    name = models.CharField(max_length=65)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SlotKind(models.Model):
    """
    A slot kind represents what kind a slot is. For example, a slot can be a
    break, lunch, or X-minute talk.
    """

    schedule = models.ForeignKey(Schedule)
    label = models.CharField(max_length=50)
    class_attr = models.CharField(max_length=50, null=True, blank=True)
    plenary = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def css_class(self):
        if not self.class_attr:
            return "slot-{}".format(self.label.lower())
        return "slot-{}".format(self.class_attr.lower())


@python_2_unicode_compatible
class Slot(models.Model):

    day = models.ForeignKey(Day)
    kind = models.ForeignKey(SlotKind)
    start = models.TimeField()
    end = models.TimeField()
    order = models.PositiveIntegerField(default=0)
    content_override = MarkupField(blank=True, default_markup_type='markdown')
    default_room = models.ForeignKey(Room, null=True, blank=True)

    video_url = models.URLField(_("video URL"), blank=True, null=True)

    keynote_url = models.URLField(_("keynote URL"), blank=True, null=True)
    keynote = models.FileField(_("keynote file"), blank=True, null=True, upload_to="keynotes")

    def assign(self, content):
        """
        Assign the given content to this slot and if a previous slot content
        was given we need to unlink it to avoid integrity errors.
        """
        self.unassign()
        content.slot = self
        content.save()

    def unassign(self):
        """
        Unassign the associated content with this slot.
        """
        content = self.content
        if content and content.slot_id:
            content.slot = None
            content.save()

    @property
    def content(self):
        """
        Return the content this slot represents.
        @@@ hard-coded for presentation for now
        """
        try:
            return self.content_ptr
        except ObjectDoesNotExist:
            return None

    def get_video_url(self):
        if self.video_url:
            return self.video_url
        try:
            return self.content_ptr.get_video_url()
        except ObjectDoesNotExist:
            pass
        return ""

    def get_keynote_url(self):
        if self.keynote and not self.keynote_url:
            return self.keynote
        elif self.keynote_url:
            return self.keynote_url
        try:
            return self.content_ptr.get_keynote_url()
        except ObjectDoesNotExist:
            pass
        return ""

    @property
    def start_datetime(self):
        return datetime.datetime(
            self.day.date.year,
            self.day.date.month,
            self.day.date.day,
            self.start.hour,
            self.start.minute)

    @property
    def end_datetime(self):
        return datetime.datetime(
            self.day.date.year,
            self.day.date.month,
            self.day.date.day,
            self.end.hour,
            self.end.minute)

    @property
    def length_in_minutes(self):
        return int(
            (self.end_datetime - self.start_datetime).total_seconds() / 60)

    @property
    def rooms(self):
        return Room.objects.filter(pk__in=self.slotroom_set.values("room"))

    def get_absolute_url(self):
        if self.content and self.content.slug:
            return reverse("schedule:slot", kwargs={"slot": self.content.slug})
        return reverse("schedule:slot", kwargs={"slot": self.pk})

    def __str__(self):
        if not self.rooms:
            return "%s %s (%s - %s)" % (self.day, self.kind, self.start, self.end)
        rooms = ", ".join(map(lambda room: room.name, self.rooms))
        return "%s %s (%s - %s, %s)" % (self.day, self.kind, self.start, self.end, rooms)

    class Meta:
        ordering = ["day", "start", "end", "default_room__order"]


@python_2_unicode_compatible
class SlotRoom(models.Model):
    """
    Links a slot with a room.
    """

    slot = models.ForeignKey(Slot)
    room = models.ForeignKey(Room)

    def __str__(self):
        return "%s %s" % (self.room, self.slot)

    class Meta:
        unique_together = [("slot", "room")]
        ordering = ["slot", "room__order"]


@python_2_unicode_compatible
class Presentation(models.Model):

    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="content_ptr", on_delete=SET_NULL)
    title = models.CharField(max_length=100, default="", blank=True)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)

    description = MarkupField(default="", blank=True, default_markup_type='markdown')
    abstract = MarkupField(default="", blank=True, default_markup_type='markdown')

    speaker = models.ForeignKey("speakers.Speaker", related_name="presentations")
    additional_speakers = models.ManyToManyField("speakers.Speaker", related_name="copresentations",
                                                 blank=True)
    cancelled = models.BooleanField(default=False)
    proposal_base = models.OneToOneField("proposals.Proposal", related_name="presentation")

    video_url = models.URLField(_("video URL"), blank=True, null=True)

    keynote_url = models.URLField(_("URL de la presentación o del código"), blank=True, null=True)
    keynote = models.FileField(_("Fichero de presentación"), blank=True, null=True, upload_to="keynotes")

    @property
    def number(self):
        return self.proposal.number

    @property
    def proposal(self):
        if self.proposal_base_id is None:
            return None
        return Proposal.objects.get_subclass(pk=self.proposal_base_id)

    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            if speaker.user:
                yield speaker

    def get_title(self):
        if self.title:
            return self.title
        return self.proposal_base.title

    def get_description(self):
        if self.description.raw:
            return self.description
        return self.proposal_base.description

    def get_abstract(self):
        if self.abstract.raw:
            return self.abstract
        return self.proposal_base.abstract

    def get_additional_notes(self):
        if self.additional_notes.raw:
            return self.additional_notes
        return self.proposal_base.additional_notes

    def get_language(self):
        return self.proposal.language

    def get_video_url(self):
        if not self.video_url:
            return ""
        return self.video_url

    def get_keynote_url(self):
        if self.keynote and not self.keynote_url:
            return self.keynote.url
        elif self.keynote_url:
            return self.keynote_url
        return ""

    def __str__(self):
        return "#%s %s (%s)" % (self.number, self.get_title(), self.speaker)

    class Meta:
        ordering = ["slot"]

    def get_api_id(self):
        return "T{:04d}".format(self.pk)

    def save(self, *args, **kwargs):
        title = self.get_title()
        if title and not self.slug:
            self.slug = slugify(title)
        super(Presentation, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Track(models.Model):
    """Tracks used in the conference."""
    name = models.TextField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    day = models.ForeignKey(Day, null=True, blank=True)

    def __str__(self):
        return self.name
