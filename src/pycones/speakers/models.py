# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Speaker(TimeStampedModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="speaker", on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_("Nombre"),
        max_length=100,
        help_text=_("Tal como quieres que apareza en el programa de la conferencia."),
    )
    biography = MarkupField(
        verbose_name=_("Biografía"),
        blank=True,
        default="",
        default_markup_type="markdown",
        help_text=_(
            "Unas palabras sobre ti. Edita usando "
            "<a href='http://warpedvisions.org/projects/"
            "markdown-cheat-sheet/target='_blank'>"
            "Markdown</a>."
        ),
    )
    photo = models.ImageField(
        verbose_name=_("Foto"), upload_to="speakers", blank=True, null=True
    )
    annotation = models.TextField(default="", blank=True)
    is_keynoter = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    @property
    def photo_url(self):
        try:
            return self.photo.url
        except ValueError:
            return static("images/default-avatar.png")

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email

    def __str__(self):
        if self.user:
            return self.name
        else:
            return "?"

    def has_biography(self):
        return bool(self.biography.raw)

    def get_api_id(self):
        return "S{:05d}".format(self.pk)

    def is_approved(self):
        """Checks if the speaker has a presentation."""
        return (
            self.proposals.filter(presentation__isnull=False).exists()
            or self.presentations.exists()
        )

    def save(self, **kwargs):
        """Save user full name by default for speaker."""
        if not self.name:
            self.name = self.user.get_full_name()
        return super(Speaker, self).save(**kwargs)
