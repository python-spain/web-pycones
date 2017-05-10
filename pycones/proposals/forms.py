# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from django.utils.translation import ugettext_lazy as _
from markupfield.widgets import MarkupTextarea
from modeltranslation.forms import TranslationModelForm

from pycones.proposals import ABSTRACT_MINIMUM_WORDS
from pycones.proposals.models import Proposal
from pycones.speakers.models import Speaker
from pycones.users.models import User
from pycones.utils.generators import random_string


class ProposalFrom(TranslationModelForm):

    speakers = forms.CharField(label=_("Ponente/s"))

    class Meta:
        model = Proposal
        fields = [
            "kind",
            "audience_level",
            "is_beginners_friendly",
            "title",
            "description",
            "abstract",
            "additional_notes",
            "language",
            "speakers"
        ]
        widgets = {
            "kind": forms.Select(attrs={"class": "form-control"}),
            "audience_level": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "abstract": MarkupTextarea(attrs={"class": "form-control"}),
            "additional_notes": MarkupTextarea(attrs={"class": "form-control"}),
            "language": forms.Select(attrs={"class": "form-control"}),
            "is_beginners_friendly": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_speakers(self):
        """Parse JSON data with speakers and creates/gets them."""
        speakers = json.loads(self.cleaned_data["speakers"])
        if not speakers:
            raise forms.ValidationError(_("Es obligatorio indicar un ponente al menos."))
        speakers_models = []
        for speaker in speakers:
            name = speaker.get("name")
            email = speaker.get("email")
            if not email and name:
                raise forms.ValidationError(_("Es falta un correo electrónico."))
            if email and not name:
                raise forms.ValidationError(_("Es falta un nombre."))
            if not email and not name:
                continue
            try:
                speaker_model = Speaker.objects.get(user__email=email)
                speaker_model.name = speaker.get("name", "")
                speaker_model.save()
            except Speaker.DoesNotExist:
                users = User.objects.filter(email=email)
                first_name = speaker.get("name", "").split(" ")[0]
                last_name = " ".join(speaker.get("name", "").split(" ")[1:])
                if not users.exists():
                    user = User.objects.create_user(
                        email=email,
                        password=random_string(),
                        first_name=first_name,
                        last_name=last_name,
                    )
                else:
                    user = users.first()
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                speaker_model = Speaker.objects.create(user=user, name=speaker.get("name", ""))
            speakers_models.append(speaker_model)
        return speakers_models

    def clean_abstract(self):
        abstract = self.cleaned_data["abstract"]
        if not abstract:
            raise forms.ValidationError(_("Este campo no puede estar vacío."))
        words = "".join(character if character.isalnum() else " " for character in abstract).split()
        if len(words) < ABSTRACT_MINIMUM_WORDS:
            raise forms.ValidationError(_("¡El resumen es demasiado corto! Tiene que tener al menos 80 palabras. "
                                          "Ayuda al equipo organizador a seleccionar "
                                          "tu charla indicando un breve esquema, si habrá demos en directo o qué "
                                          "conocimientos previos debería tener la audiencia"))
        return abstract

    def save(self, commit=True):
        proposal = super(ProposalFrom, self).save(commit=False)
        proposal.save()
        speakers = self.cleaned_data["speakers"]
        proposal.speakers.clear()
        proposal.speakers.add(*speakers)
        if not proposal.notified:
            proposal.notify()
        return proposal


class EditProposalFrom(ProposalFrom):

    def save(self, commit=True):
        return super(ProposalFrom, self).save(commit=commit)
