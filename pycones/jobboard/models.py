# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from markupfield.fields import MarkupField


class JobOffer(TimeStampedModel):
    """A job offer published by a sponsor"""

    employer = models.ForeignKey(
        "sponsorships.Sponsor", related_name="employer", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, verbose_name=_("Título"))
    description = MarkupField(
        _("Descripción"),
        blank=True,
        default="",
        default_markup_type="markdown",
        help_text=_("Describe de job offer"),
    )
    application_url = models.URLField(_("Application URL"))

