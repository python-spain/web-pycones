# -*- coding: utf-8 -*-


from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from pycones.sponsorships import (
    BENEFIT_WEB_LOGO,
    BENEFIT_TYPE_CHOICES,
    BENEFIT_SIMPLE,
    BENEFIT_FILE,
    BENEFIT_TEXT,
)
from pycones.sponsorships.managers import SponsorManager


class SponsorLevel(models.Model):

    name = models.CharField(_("name"), max_length=100)
    order = models.IntegerField(_("order"), default=0)
    cost = models.PositiveIntegerField(_("cost"))
    description = models.TextField(
        _("description"), blank=True, help_text=_("This is private.")
    )

    class Meta:
        ordering = ["order"]
        verbose_name = _("sponsor level")
        verbose_name_plural = _("sponsor levels")

    def __str__(self):
        return self.name

    def sponsors(self):
        return self.sponsor_set.filter(active=True).order_by("added")


class Sponsor(TimeStampedModel):

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sponsorships",
        verbose_name=_("applicant"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Sponsor Name"), max_length=100)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(
        _("Contact Name"), max_length=100, null=True, blank=True
    )
    contact_email = models.EmailField(_("Contact Email"), null=True, blank=True)
    level = models.ForeignKey(
        SponsorLevel, verbose_name=_("level"), on_delete=models.CASCADE
    )

    active = models.BooleanField(_("active"), default=False)
    sponsor_logo = models.ForeignKey(
        "SponsorBenefit",
        related_name="+",
        null=True,
        blank=True,
        editable=False,
        on_delete=models.CASCADE,
    )  # Denormalization (this assumes only one logo)
    sponsor_order = models.IntegerField(
        help_text=_("Relative order of the sponsor"), default=0
    )

    objects = SponsorManager()

    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")

    @property
    def website_logo(self):
        if self.sponsor_logo is None:
            benefits = self.sponsor_benefits.filter(
                benefit__type=BENEFIT_WEB_LOGO, upload__isnull=False
            )[:1]
            if benefits.count():
                if benefits[0].upload and benefits[0].upload.name:
                    self.sponsor_logo = benefits[0]
                    self.save()
                else:
                    return None
        return self.sponsor_logo.upload

    @property
    def listing_text(self):
        if not hasattr(self, "_listing_text"):
            self._listing_text = None
            # @@@ better than hard-coding a pk but still not good
            benefits = self.sponsor_benefits.filter(benefit__name="Sponsor Description")
            if benefits.count():
                self._listing_text = benefits[0].text
        return self._listing_text

    def __str__(self):
        return self.name

    def reset_benefits(self):
        """
        Reset all benefits for this sponsor to the defaults for their
        sponsorship level.
        """
        level = None

        try:
            level = self.level
        except SponsorLevel.DoesNotExist:
            pass

        allowed_benefits = []
        if level:
            for benefit_level in level.benefit_levels.all():
                # Create all needed benefits if they don't exist already
                sponsor_benefit, created = SponsorBenefit.objects.get_or_create(
                    sponsor=self, benefit=benefit_level.benefit
                )

                # and set to default limits for this level.
                sponsor_benefit.max_words = benefit_level.max_words
                sponsor_benefit.other_limits = benefit_level.other_limits

                # and set to active
                sponsor_benefit.active = True

                # @@@ We don't call sponsor_benefit.clean here. This means
                # that if the sponsorship level for a sponsor is adjusted
                # downwards, an existing too-long text entry can remain,
                # and won't raise a validation error until it's next
                # edited.
                sponsor_benefit.save()

                allowed_benefits.append(sponsor_benefit.pk)

        # Any remaining sponsor benefits that don't normally belong to
        # this level are set to inactive
        self.sponsor_benefits.exclude(pk__in=allowed_benefits).update(
            active=False, max_words=None, other_limits=""
        )

    def send_coordinator_emails(self):
        pass  # @@@ should this just be done centrally?


class Benefit(models.Model):

    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    type = models.CharField(
        _("type"), choices=BENEFIT_TYPE_CHOICES, max_length=10, default=BENEFIT_SIMPLE
    )

    def __str__(self):
        return self.name


class BenefitLevel(models.Model):

    benefit = models.ForeignKey(
        Benefit,
        related_name="benefit_levels",
        verbose_name=_("benefit"),
        on_delete=models.CASCADE,
    )
    level = models.ForeignKey(
        SponsorLevel,
        related_name="benefit_levels",
        verbose_name=_("level"),
        on_delete=models.CASCADE,
    )

    # default limits for this benefit at given level
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)

    class Meta:
        ordering = ["level"]

    def __str__(self):
        return "%s - %s" % (self.level, self.benefit)


class SponsorBenefit(models.Model):

    sponsor = models.ForeignKey(
        Sponsor,
        related_name="sponsor_benefits",
        verbose_name=_("sponsor"),
        on_delete=models.CASCADE,
    )
    benefit = models.ForeignKey(
        Benefit,
        related_name="sponsor_benefits",
        verbose_name=_("benefit"),
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(default=True)

    # Limits: will initially be set to defaults from corresponding BenefitLevel
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)

    # Data: zero or one of these fields will be used, depending on the
    # type of the Benefit (text, file, or simple)
    text = models.TextField(_("text"), blank=True)
    upload = models.FileField(_("file"), blank=True, upload_to="sponsor_files")

    class Meta:
        ordering = ["-active"]

    def __str__(self):
        return "%s - %s" % (self.sponsor, self.benefit)

    def clean(self):
        num_words = len(self.text.split())
        if self.max_words and num_words > self.max_words:
            raise ValidationError(
                "Sponsorship level only allows for %s words, you provided %d."
                % (self.max_words, num_words)
            )

    def data_fields(self):
        """
        Return list of data field names which should be editable for
        this ``SponsorBenefit``, depending on its ``Benefit`` type.
        """
        if self.benefit.type == BENEFIT_FILE or self.benefit.type == BENEFIT_WEB_LOGO:
            return ["upload"]
        elif self.benefit.type == BENEFIT_TEXT:
            return ["text"]
        return []
