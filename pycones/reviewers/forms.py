# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from pycones.reviewers import REVIEW_GROUP_NAME
from pycones.reviewers.helpers import create_reviews
from pycones.reviewers.models import Review, Reviewer
from pycones.speakers.models import Speaker
from pycones.users.models import User
from pycones.utils.generators import random_string


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["score", "notes", "conflict", "finished"]
        widgets = {
            "score": forms.NumberInput(attrs={"class": "form-control", "min": "1", "max": "4", "step": "0.1"}),
            "notes": forms.Textarea(attrs={"class": "form-control"}),
            "conflict": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "finished": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_score(self):
        score = self.cleaned_data.get("score")
        if score is None:
            return score
        if 0.0 >= score or score > 4.0:
            raise forms.ValidationError(_("Debes puntuar entre 1.0 y 4.0"))
        return round(score, 1)


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
        if user in [speaker.user for speaker in proposal.speakers.all()]:
            raise forms.ValidationError("You can not assign a review to its author!")


class ReviewerSignUpForm(forms.Form):
    """Form to allow a user to be registered as a reviewer. It should
    work in the same than the case the user wants to restore his
    password.
    """

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Speaker.objects.filter(user__email=email).exists():
            raise forms.ValidationError(_("Un posible ponente no puede registrarse como revisor."))
        if Reviewer.objects.filter(user__email=email):
            raise forms.ValidationError(_("Ya estás registrado como revisor."))
        return email

    def save(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        else:
            try:
                user = User.objects.create_user(email=email, password=random_string())
            except IntegrityError:
                user = User.objects.get(email=email)
        # Create reviewer profile
        group = Group.objects.get(name=REVIEW_GROUP_NAME)
        if group not in user.groups.all():
            user.groups.add(group)
        # Sends restore password
        user.send_restore_password_link()
        create_reviews(user)
        return user


class ReviewsFilterForm(forms.Form):

    only_unfinished = forms.BooleanField(
        label=_("Mostrar sólo revisiones no terminadas"),
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
