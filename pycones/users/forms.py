# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from pycones.users.models import User


class SignInForm(forms.Form):
    """Form for handle in a user can log in."""

    email = forms.fields.EmailField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Email"),
            "autocapitalize": "off",
            "autocorrect": "off",
            "autofocus": "autofocus",
        }),
        error_messages={'required': _('El email es obligatorio')}
    )
    password = forms.fields.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": _("Contraseña")
        }),
        error_messages={'required': _('La contraseña es obligatoria')}
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("El email no existe"))
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError(_("La contraseña no es correcta"))
        except User.DoesNotExist:
            pass
        return password


class RestorePasswordForm(forms.Form):

    email = forms.EmailField(label=_("Email"), widget=forms.HiddenInput())
    restore_code = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": _("Contraseña"),
        }
    ))
    repeat_password = forms.CharField(label=_("Repita la contraseña"), widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": _("Repita la contraseña"),
        }
    ))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("El email no existe"))
        return email

    def clean_repeat_password(self):
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("repeat_password")
        if password != repeat_password:
            raise forms.ValidationError(_("Las contraseñas no son iguales"))
        return repeat_password

    def clean_restore_code(self):
        email = self.cleaned_data.get("email")
        restore_code = self.cleaned_data.get("restore_code")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Código de restauración no válido"))
        user = User.objects.get(email=email)
        if user.restore_code != restore_code:
            raise forms.ValidationError(_("Código de restauración no válido"))
        return restore_code


class RequestRestoreCodeForm(forms.Form):

    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": _("Email"),
    }))


