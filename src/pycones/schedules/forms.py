# -*- coding: utf-8 -*-
from django import forms

from pycones.schedules.models import Presentation


class PresentationForm(forms.ModelForm):

    class Meta:
        model = Presentation
        fields = ["keynote", "keynote_url"]
        widgets = {
            "keynote_url": forms.TextInput(attrs={"class": "form-control"})
        }
