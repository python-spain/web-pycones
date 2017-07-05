# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from collections import OrderedDict

import six
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import SET_NULL
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.timezone import make_aware
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField


@python_2_unicode_compatible
class Day(models.Model):

    date = models.DateField(unique=True)

    def __str__(self):
        return "%s" % self.date

    class Meta:
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

    name = models.CharField(max_length=65)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Track(models.Model):
    """Tracks used in the conference."""
    name = models.TextField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    day = models.ForeignKey(Day, null=True, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SlotKind(models.Model):
    """A slot kind represents what kind a slot is. For example, a slot can be a
    break, lunch, or X-minute talk.
    """

    label = models.CharField(max_length=50)
    class_attr = models.CharField(max_length=50, null=True, blank=True)
    plenary = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def css_class(self):
        if not self.class_attr:
            return "slot-{}".format(self.label_en.lower())
        return "slot-{}".format(self.class_attr.lower())


@python_2_unicode_compatible
class Slot(models.Model):

    day = models.ForeignKey(Day)
    kind = models.ForeignKey(SlotKind)
    start = models.TimeField()
    end = models.TimeField()
    order = models.PositiveIntegerField(default=0)
    content_override = MarkupField(blank=True, default_markup_type='markdown')

    room = models.ForeignKey(Room, related_name="slots", null=True, blank=True)
    track = models.ForeignKey(Track, related_name="slots", null=True, blank=True)

    video_url = models.URLField(_("video URL"), blank=True, null=True)
    keynote_url = models.URLField(_("keynote URL"), blank=True, null=True)
    keynote = models.FileField(_("keynote file"), blank=True, null=True, upload_to="keynotes")

    class Meta:
        ordering = ["day", "start", "end", "track__order", "order"]

    @property
    def content(self):
        """ Return the content this slot represents."""
        try:
            return self.presentation
        except ObjectDoesNotExist:
            return None

    @property
    def start_datetime(self):
        return make_aware(
            datetime.datetime(
                self.day.date.year,
                self.day.date.month,
                self.day.date.day,
                self.start.hour,
                self.start.minute
            )
        )

    @property
    def end_datetime(self):
        return make_aware(
            datetime.datetime(
                self.day.date.year,
                self.day.date.month,
                self.day.date.day,
                self.end.hour,
                self.end.minute
            )
        )

    def __str__(self):
        return "%s %s (%s - %s, %s)" % (self.day, self.kind, self.start, self.end, self.room)

    def assign(self, content):
        """Assign the given content to this slot and if a previous slot content
        was given we need to unlink it to avoid integrity errors.
        """
        self.unassign()
        content.slot = self
        content.save()

    def unassign(self):
        """Unassign the associated content with this slot."""
        content = self.presentation
        if content and content.slot_id:
            content.slot = None
            content.save()

    def get_video_url(self):
        if self.video_url:
            return self.video_url
        try:
            return self.presentation.get_video_url()
        except ObjectDoesNotExist:
            pass
        return ""

    def get_keynote_url(self):
        if self.keynote and not self.keynote_url:
            return self.keynote
        elif self.keynote_url:
            return self.keynote_url
        try:
            return self.presentatione.get_keynote_url()
        except ObjectDoesNotExist:
            pass
        return ""

    def get_absolute_url(self):
        if self.content and self.content.slug:
            return reverse("schedule:slot", kwargs={"slot": self.content.slug})
        return reverse("schedule:slot", kwargs={"slot": self.pk})


@python_2_unicode_compatible
class Presentation(models.Model):

    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="presentation", on_delete=SET_NULL)

    title = models.CharField(max_length=100, default="", blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, allow_unicode=True)
    description = MarkupField(default="", blank=True, default_markup_type='markdown')
    abstract = MarkupField(default="", blank=True, default_markup_type='markdown')

    speakers = models.ManyToManyField("speakers.Speaker", related_name="presentations", blank=True)
    proposal = models.OneToOneField("proposals.Proposal", related_name="presentation")

    cancelled = models.BooleanField(default=False)

    video_url = models.URLField(_("video URL"), blank=True, null=True)
    keynote_url = models.URLField(_("URL de la presentación o del código"), blank=True, null=True)
    keynote = models.FileField(_("Fichero de presentación"), blank=True, null=True, upload_to="keynotes")

    class Meta:
        ordering = ["slot"]

    def __str__(self):
        return "#%s %s (%s)" % (self.pk, self.get_title(), ",".join(map(lambda s: six.text_type(s), self.get_speakers())))

    def get_title(self):
        if self.title:
            return self.title
        return self.proposal.title

    def get_description(self):
        if self.description.raw:
            return self.description
        return self.proposal.description

    def get_abstract(self):
        if self.abstract.raw:
            return self.abstract
        return self.proposal.abstract

    def get_additional_notes(self):
        if self.additional_notes.raw:
            return self.additional_notes
        return self.proposal.additional_notes

    def get_language(self):
        return self.proposal.language

    def get_speakers(self):
        if self.speakers.exists():
            return self.speakers.all()
        return self.proposal.speakers.all()

    def get_audience_level(self):
        return self.proposal.audience_level

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

    def get_api_id(self):
        return "T{:04d}".format(self.pk)

    def save(self, *args, **kwargs):
        title = self.get_title()
        if title and not self.slug:
            self.slug = slugify(title)
        super(Presentation, self).save(*args, **kwargs)


