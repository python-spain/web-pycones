# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from pycones.reviewers import REVIEW_GROUP_NAME
from pycones.reviewers.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["relevance", "interest", "newness", "notes", "conflict", "finished"]
        widgets = {
            "relevance": forms.NumberInput(attrs={"class": "form-control",
                                                  "min": "1", "max": "10", "step": "1"}),
            "interest": forms.NumberInput(attrs={"class": "form-control",
                                                 "min": "1", "max": "10", "step": "1"}),
            "newness": forms.NumberInput(attrs={"class": "form-control",
                                                "min": "1", "max": "10", "step": "1"}),
            "notes": forms.Textarea(attrs={"class": "form-control"}),
        }

    @staticmethod
    def _clean_metric(metric):
        if metric is None:
            return metric
        if 0 >= metric or metric > 10:
            raise forms.ValidationError(_("Debes puntuar entre 1 y 10"))
        return metric

    def clean_interest(self):
        interest = self.cleaned_data.get("interest")
        return self._clean_metric(interest)

    def clean_relevance(self):
        relevance = self.cleaned_data.get("relevance")
        return self._clean_metric(relevance)

    def clean_newness(self):
        newness = self.cleaned_data.get("newness")
        return self._clean_metric(newness)


class ReviewAdminForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ReviewAdminForm, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = get_user_model().objects.filter(
            Q(groups__name=REVIEW_GROUP_NAME) | Q(is_superuser=True)
        )

    def clean(self):
        cleaned_data = super(ReviewAdminForm, self).clean()
        user = cleaned_data.get("user")
        proposal = cleaned_data.get("proposal")
        if user == proposal.speaker.user:
            raise forms.ValidationError("You can not assign a review to its author!")
