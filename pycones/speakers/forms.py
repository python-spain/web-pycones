# -*- coding: utf-8 -*-
from django import forms
from markupfield.widgets import AdminMarkupTextareaWidget

from pycones.speakers.models import Speaker


class SpeakerForm(forms.ModelForm):

    class Meta:
        model = Speaker
        fields = ["name", "email", "biography", "photo"]
        widgets = {
            "biography": AdminMarkupTextareaWidget(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
