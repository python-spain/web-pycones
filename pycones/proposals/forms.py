# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from markupfield.widgets import MarkupTextarea

from modeltranslation.forms import TranslationModelForm


from pycones.proposals.models import Proposal
from pycones.speakers.models import Speaker
from pycones.utils.generators import random_string


class ProposalFrom(TranslationModelForm):

    speaker_name = forms.CharField(
        label=_("Nombre del ponente"),
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    speaker_email = forms.EmailField(
        label=_("Email del ponente"),
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Proposal
        exclude = [
            "speaker",
            "additional_speakers",
            "cancelled",
            "duration",
            "additional_notes_markup_type",
            "additional_notes_es_markup_type",
            "additional_notes_en_markup_type",
            "additional_notes_ca_markup_type",
            "additional_notes_eu_markup_type",
            "additional_notes_gl_markup_type",
            "abstract_markup_type",
            "abstract_es_markup_type",
            "abstract_en_markup_type",
            "abstract_ca_markup_type",
            "abstract_eu_markup_type",
            "abstract_gl_markup_type",
            "code"
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
        if len(words) < 80:
            raise forms.ValidationError(_("¡El resumen es demasiado corto! Tiene que tener al menos 80 palabras. "
                                          "Ayuda al equipo organizador a seleccionar "
                                          "tu charla indicando un breve esquema, si habrá demos en directo o qué "
                                          "conocimientos previos debería tener la audiencia"))
        return abstract

    def get_speaker(self):
        name = self.cleaned_data.get("speaker_name", "")
        email = self.cleaned_data.get("speaker_email")
        try:
            speaker = Speaker.objects.get(user__email=email)
        except Speaker.DoesNotExist:
            user = User.objects.create_user(
                email=email, first_name=name[:30], password=random_string()
            )
            speaker = Speaker.objects.create(
                user=user, name=name[:100],
                biography="", biography_markup_type='markdown',
                biography_es="", biography_es_markup_type='markdown',
                biography_en="", biography_en_markup_type='markdown',
                biography_ca="", biography_ca_markup_type='markdown',
                biography_eu="", biography_eu_markup_type='markdown',
                biography_gl="", biography_gl_markup_type='markdown',
            )
        return speaker

    def save(self, commit=True):
        proposal = super(ProposalFrom, self).save(commit=False)
        proposal.speaker = self.get_speaker()
        proposal.abstract_markup_type = 'markdown'
        proposal.abstract_es_markup_type = 'markdown'
        proposal.abstract_en_markup_type = 'markdown'
        proposal.abstract_ca_markup_type = 'markdown'
        proposal.abstract_eu_markup_type = 'markdown'
        proposal.abstract_gl_markup_type = 'markdown'
        proposal.additional_notes_markup_type = 'markdown'
        proposal.additional_notes_en_markup_type = 'markdown'
        proposal.additional_notes_es_markup_type = 'markdown'
        proposal.additional_notes_ca_markup_type = 'markdown'
        proposal.additional_notes_eu_markup_type = 'markdown'
        proposal.additional_notes_gl_markup_type = 'markdown'
        proposal.save()
        if not proposal.notified:
            proposal.notify()
        return proposal


class EditProposalFrom(ProposalFrom):

    def get_speaker(self):
        speaker = self.instance.speaker
        name = self.cleaned_data.get("speaker_name", "")
        email = self.cleaned_data.get("speaker_email")
        speaker.name = name
        speaker.user.email = email
        speaker.user.save()
        speaker.save()
        return speaker

    def save(self, commit=True):
        self.get_speaker()
        return super(ProposalFrom, self).save(commit=commit)
