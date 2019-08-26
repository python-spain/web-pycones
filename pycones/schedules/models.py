# -*- coding: utf-8 -*-


import datetime
from collections import OrderedDict

import six
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db import models
from django.db.models import SET_NULL
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.timezone import make_aware
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField

from pycones.proposals import BASIC_LEVEL, PROPOSAL_LANGUAGES


class Day(models.Model):

    date = models.DateField(unique=True)

    def __str__(self):
        return "%s" % self.date

    class Meta:
        ordering = ["date"]

    def slots(self):
        return self.slot_set.all().order_by("order")

    def tracks(self):
        return self.track_set.all().order_by("name")

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


class Room(models.Model):

    name = models.CharField(max_length=65)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Track(models.Model):
    """Tracks used in the conference."""

    name = models.TextField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    day = models.ForeignKey(Day, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
            return "slot-{}".format(self.label.lower())
        return "slot-{}".format(self.class_attr.lower())


class Slot(models.Model):

    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    kind = models.ForeignKey(SlotKind, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()
    order = models.PositiveIntegerField(default=0)
    content_override = MarkupField(blank=True, default_markup_type="markdown")

    room = models.ForeignKey(
        Room, related_name="slots", null=True, blank=True, on_delete=models.CASCADE
    )
    track = models.ForeignKey(
        Track, related_name="slots", null=True, blank=True, on_delete=models.CASCADE
    )

    video_url = models.URLField(_("video URL"), blank=True, null=True)
    keynote_url = models.URLField(_("keynote URL"), blank=True, null=True)
    keynote = models.FileField(
        _("keynote file"), blank=True, null=True, upload_to="keynotes"
    )

    class Meta:
        ordering = ["day", "start", "end", "track__order", "order"]

    @property
    def content(self):
        """ Return the content this slot represents."""
        try:
            return self.presentation
        except ObjectDoesNotExist:
            return self.content_override

    @property
    def title(self):
        try:
            c = self.presentation
            return c.get_title()
        except ObjectDoesNotExist:
            return ""

    @property
    def description(self):
        try:
            c = self.presentation
            return c.get_description()
        except ObjectDoesNotExist:
            return self.content_override

    @property
    def start_datetime(self):
        return make_aware(
            datetime.datetime(
                self.day.date.year,
                self.day.date.month,
                self.day.date.day,
                self.start.hour,
                self.start.minute,
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
                self.end.minute,
            )
        )

    @property
    def duration(self):
        return (self.end_datetime - self.start_datetime) // 60

    def __str__(self):
        return "%s %s (%s - %s, %s)" % (
            self.day,
            self.kind,
            self.start,
            self.end,
            self.room,
        )

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
            return self.presentation.get_keynote_url()
        except ObjectDoesNotExist:
            pass
        return ""

    def get_absolute_url(self):
        if self.content and self.content.slug:
            return reverse("schedule:slot", kwargs={"slot": self.content.slug})
        return reverse("schedule:slot", kwargs={"slot": self.pk})


class Presentation(models.Model):

    slot = models.OneToOneField(
        Slot, null=True, blank=True, related_name="presentation", on_delete=SET_NULL
    )

    title = models.CharField(max_length=100, default="", blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, allow_unicode=True)
    description = MarkupField(default="", blank=True, default_markup_type="markdown")
    abstract = MarkupField(default="", blank=True, default_markup_type="markdown")
    language = models.CharField(
        verbose_name=_("Idioma"),
        max_length=2,
        choices=PROPOSAL_LANGUAGES,
        null=True,
        blank=True,
    )

    speakers = models.ManyToManyField(
        "speakers.Speaker", related_name="presentations", blank=True
    )
    proposal = models.OneToOneField(
        "proposals.Proposal",
        related_name="presentation",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    cancelled = models.BooleanField(default=False)

    video_url = models.URLField(_("video URL"), blank=True, null=True)
    keynote_url = models.URLField(
        _("URL de la presentación o del código"), blank=True, null=True
    )
    keynote = models.FileField(
        _("Fichero de presentación"), blank=True, null=True, upload_to="keynotes"
    )

    class Meta:
        ordering = ["slot"]

    def __str__(self):
        return "#%s %s (%s)" % (
            self.pk,
            self.get_title(),
            ",".join(map(lambda s: six.text_type(s), self.get_speakers())),
        )

    def get_title(self):
        if self.title:
            return self.title
        if self.proposal:
            return self.proposal.title
        return None

    def get_description(self):
        if self.description.raw:
            return self.description
        if self.proposal:
            return self.proposal.description
        return None

    def get_abstract(self):
        if self.abstract.raw:
            return self.abstract
        if self.proposal:
            return self.proposal.translated_abstract
        return None

    def get_additional_notes(self):
        if self.additional_notes.raw:
            return self.additional_notes
        if self.proposal:
            return self.proposal.translated_additional_notes
        return None

    def get_language(self):
        if self.language:
            return self.language
        if self.proposal:
            return self.proposal.language
        return None

    def get_speakers(self):
        if self.speakers.exists():
            return self.speakers.all()
        if self.proposal:
            return self.proposal.speakers.all()
        return self.speakers.all()

    def has_speakers(self):
        return self.get_speakers().exists()

    def get_audience_level(self):
        if self.proposal:
            return self.proposal.audience_level
        return BASIC_LEVEL

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

