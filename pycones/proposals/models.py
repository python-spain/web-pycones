# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from taggit_autosuggest.managers import TaggableManager

from pycones.proposals import PROPOSAL_LEVELS, BASIC_LEVEL, PROPOSAL_LANGUAGES, PROPOSAL_DURATIONS
from pycones.reviewers.models import Reviewer
from pycones.utils.emails import send_email
from pycones.utils.generators import random_string
from pycones.utils.translations import get_translated_markdown_field


@python_2_unicode_compatible
class ProposalKind(models.Model):

    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Proposal(TimeStampedModel):

    audience_level = models.CharField(
        verbose_name=_("Nivel de la audiencia"),
        choices=PROPOSAL_LEVELS,
        null=True,
        default=BASIC_LEVEL,
        max_length=32
    )
    language = models.CharField(
        verbose_name=_("Idioma"),
        max_length=2,
        choices=PROPOSAL_LANGUAGES,
        default="es"
    )
    duration = models.PositiveIntegerField(
        verbose_name=_("Duración"),
        choices=PROPOSAL_DURATIONS,
        default=30,
        null=True,
        blank=True
    )
    tags = TaggableManager(
        verbose_name=_("Etiquetas"),
        help_text=_("Lista de etiquetas separadas por comas."),
        blank=True
    )

    is_beginners_friendly = models.BooleanField(
        verbose_name=_("¿Es apta para principiantes?"),
        default=False
    )

    kind = models.ForeignKey("proposals.ProposalKind", verbose_name=_("Tipo de propuesta"))

    title = models.CharField(max_length=100, verbose_name=_("Título"))
    description = models.TextField(
        _("Breve descripción"),
        max_length=500,
        help_text=_("Si tu propuesta se acepta esto se hará público, y se incluirá en el programa. "
                    "Debería ser un párrafo, con un máximo de 500 caracteres.")
    )
    abstract = MarkupField(
        _("Resumen detallado"),
        blank=True,
        default="",
        default_markup_type='markdown',
        help_text=_("Resumen detallado. Se hará pública si la propuesta se acepta. Edita "
                    "usando <a href='http://daringfireball.net/projects/markdown/basics' "
                    "target='_blank'>Markdown</a>.")
    )
    additional_notes = MarkupField(
        _("Notas adicionales"),
        blank=True,
        default="",
        default_markup_type='markdown',
        help_text=_("Cualquier cosa que te gustaría hacer saber a los revisores para que la tengan en "
                    "cuenta al ahora de hacer la selección. Esto no se hará público. Edita usando "
                    "<a href='http://daringfireball.net/projects/markdown/basics' "
                    "target='_blank'>Markdown</a>.")
    )

    speakers = models.ManyToManyField("speakers.Speaker", related_name="proposals", blank=False)

    cancelled = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)
    accepted = models.NullBooleanField(verbose_name=_('Aceptada'), default=None)
    accepted_notified = models.BooleanField(verbose_name=_('Notificación de aceptación enviada'), default=False)
    code = models.CharField(max_length=64, null=True, blank=True)

    @property
    def translated_abstract(self):
        return get_translated_markdown_field(self, "abstract")

    @property
    def translated_additional_notes(self):
        return get_translated_markdown_field(self, "additional_notes")

    @property
    def avg(self):
        data = [review.avg() for review in self.reviews.filter(finished=True) if review.avg() is not None]
        if data:
            return sum(data) / len(data)
        return None

    @property
    def completed_reviews(self):
        return self.reviews.filter(finished=True).count()

    @property
    def assigned_reviews(self):
        return self.reviews.count()

    @property
    def tag_list(self):
        return ", ".join(tag.name for tag in self.tags.all())

    @property
    def speakers_list(self):
        return ", ".join(["%s <%s>" % (speaker.name, speaker.email) for speaker in self.speakers.all()])

    @property
    def renormalization_o0(self):
        """Renormalization with order 0. Average value of 0"""
        relevance, interest, newness = [], [], []
        for review in self.reviews.all():
            reviewer = Reviewer.objects.get(user=review.user)
            mean = reviewer.mean()
            if reviewer.num_reviews() <= 1:
                continue
            relevance.append((review.relevance or 0) - mean)
            interest.append((review.interest or 0) - mean)
            newness.append((review.newness or 0) - mean)
        return np.mean(interest + relevance + newness)

    @property
    def renormalization_o1(self):
        """Renormalization with order 1. Expand the value to get the same standard deviation for everyone"""
        relevance, interest, newness = [], [], []
        for review in self.reviews.all():
            reviewer = Reviewer.objects.get(user=review.user)
            std = reviewer.std()
            if reviewer.num_reviews() <= 1 or std < 0.75:
                continue
            relevance.append((review.relevance or 0) - std)
            interest.append((review.interest or 0) - std)
            newness.append((review.newness or 0) - std)
        return np.mean(interest + relevance + newness)

    def notification_email_context(self, speaker):
        site = Site.objects.get_current()
        return {
            "title": self.title,
            "speaker": speaker,
            "kind": self.kind.name,
            "code": self.code,
            "site": site,
        }

    def notify(self):
        """Sends an email to the creator of the proposal with a confirmation email. The emails has a
        link to edit the proposal.
        """
        if not self.code:
            self.code = random_string(64)
        for speaker in self.speakers.all():
            context = self.notification_email_context(speaker=speaker)
            send_email(
                context=context,
                template="emails/proposals/confirmation.html",
                subject=_("[%s] Confirmación de propuesta de charla") % settings.CONFERENCE_TITLE,
                to=speaker.email,
                from_email=settings.CONTACT_EMAIL
            )
        self.notified = True
        self.save()

    def notify_acceptance(self):
        """Sends an email to the creator of the proposal with an email with the resolution of the acceptance or not
        of his proposal.
        """
        for speaker in self.speakers.all():
            context = self.notification_email_context(speaker=speaker)
            if self.accepted is None:
                return
            template = "emails/proposals/accepted.html" if self.accepted else "emails/proposals/rejected.html"
            send_email(
                context=context,
                template=template,
                subject=_("[%s] Notificación de propuesta de charla") % settings.CONFERENCE_TITLE,
                to=self.speaker.email,
                from_email=settings.CONTACT_EMAIL
            )
        self.accepted_notified = True
        self.save()
