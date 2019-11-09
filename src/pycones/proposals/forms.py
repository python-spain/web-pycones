# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from django.utils.translation import ugettext_lazy as _
from modeltranslation.forms import TranslationModelForm


from pycones.proposals import ABSTRACT_MINIMUM_WORDS
from pycones.proposals.models import Proposal
from pycones.speakers.models import Speaker
from pycones.users.models import User
from pycones.utils.generators import random_string
from martor.fields import MartorFormField


class ProposalFrom(TranslationModelForm):

    speaker_name = forms.CharField(label=_("Ponente/s"))
    speaker_email = forms.EmailField(label=_("Email"))
    description = MartorFormField()
    abstract = MartorFormField()
    additional_notes = MartorFormField()

    class Meta:
        model = Proposal
        fields = [
            "kind",
            "duration",
            "audience_level",
            "is_beginners_friendly",
            "title",
            "description",
            "abstract",
            "additional_notes",
            "language",
        ]
        widgets = {
            "speaker_name": forms.TextInput(attrs={"class": "form-control"}),
            "speaker_email": forms.TextInput(attrs={"class": "form-control"}),
            "duration": forms.Select(
                attrs={"class": "form-control", "required": "required"}
            ),
            "kind": forms.Select(attrs={"class": "form-control"}),
            "audience_level": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "language": forms.Select(attrs={"class": "form-control"}),
            "is_beginners_friendly": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def return_speaker(self, name, email):
        """Parse JSON data with speakers and creates/gets them."""
        if not email and name:
            raise forms.ValidationError(_("Es falta un correo electrónico."))
        if email and not name:
            raise forms.ValidationError(_("Es falta un nombre."))
        if not email and not name:
            raise forms.ValidationError(_("Falta todo"))

        user = User.objects.filter(email=email)

        if not user.exists():
            first_name = name.split(" ")[0]
            last_name = " ".join(name.split(" ")[1:])
            user = User.objects.create_user(
                email=email,
                password=random_string(),
                first_name=first_name,
                last_name=last_name,
            )
            speaker = Speaker(user=user, name=name)
            speaker.save()
        else:
            user = user.first()
            speaker = Speaker.objects.get(user=user)

        return speaker

    def clean_abstract(self):
        abstract = self.cleaned_data["abstract"]
        if not abstract:
            raise forms.ValidationError(_("Este campo no puede estar vacío."))
        words = "".join(
            character if character.isalnum() else " " for character in abstract
        ).split()
        if len(words) < ABSTRACT_MINIMUM_WORDS:
            raise forms.ValidationError(
                _(
                    "¡El resumen es demasiado corto! Tiene que tener al menos 80 palabras. "
                    "Ayuda al equipo organizador a seleccionar "
                    "tu charla indicando un breve esquema, si habrá demos en directo o qué "
                    "conocimientos previos debería tener la audiencia"
                )
            )
        return abstract

    def save(self, commit=True):
        proposal = super(ProposalFrom, self).save(commit=False)
        proposal.save()
        speaker = self.return_speaker(
            self.cleaned_data["speaker_name"], self.cleaned_data["speaker_email"]
        )
        proposal.speakers.clear()
        proposal.speakers.add(speaker)
        if not proposal.notified:
            proposal.notify()
        return proposal


class EditProposalFrom(ProposalFrom):
    def save(self, commit=True):
        return super(ProposalFrom, self).save(commit=commit)
