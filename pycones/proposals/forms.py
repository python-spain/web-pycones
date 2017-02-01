# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from markupfield.widgets import MarkupTextarea

from modeltranslation.forms import TranslationModelForm

from pycones.proposals import ABSTRACT_MINIMUM_WORDS
from pycones.proposals.models import Proposal
from pycones.speakers.models import Speaker
from pycones.utils.generators import random_string


class ProposalFrom(TranslationModelForm):

    class Meta:
        model = Proposal
        fields = [
            "kind",
            "audience_level",
            "title",
            "description",
            "abstract",
            "additional_notes",
            "language",
        ]
        widgets = {
            "kind": forms.Select(attrs={"class": "form-control"}),
            "audience_level": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "abstract": MarkupTextarea(attrs={"class": "form-control"}),
            "additional_notes": MarkupTextarea(attrs={"class": "form-control"}),
            "language": forms.Select(attrs={"class": "form-control"}),
        }

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
        if not proposal.notified:
            proposal.notify()
        return proposal


class EditProposalFrom(ProposalFrom):

    def save(self, commit=True):
        return super(ProposalFrom, self).save(commit=commit)
