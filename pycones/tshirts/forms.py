#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _

from pycones.tshirts.models import TshirtBooking


class EntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add some classes to the inputs
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-2 input-lg'})
        self.fields['booking_id'].widget.attrs.update({'class': "form-control mb-5 input-lg"})

    def clean(self):
        """ Verifies that the given email and and booking id actually exist. """

        # Obtain the cleaned data
        cleaned_data = self.cleaned_data

        # Make sure we've got a reserve with this data, add error an otherwise
        if not TshirtBooking.objects.filter(
                email=cleaned_data['email'], booking_id=cleaned_data['booking_id']).exists():
            self.add_error(None, _('No hemos podido encontrar su reserva con los datos proporcionados.'))

        # Return the cleaned data
        return cleaned_data

    class Meta:
        model = TshirtBooking
        fields = ('email', 'booking_id', )


class TShirtForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the fields required
        self.fields['nif'].required = True
        self.fields['sex'].required = True
        self.fields['tshirt_size'].required = True

        # Add some classes to the inputs
        self.fields['nif'].widget.attrs.update({'class': 'form-control mb-2 input-lg'})
        self.fields['sex'].widget.attrs.update({'class': 'form-control mb-5 input-lg'})
        self.fields['tshirt_size'].widget.attrs.update({'class': 'form-control mb-5 input-lg'})

    class Meta:
        model = TshirtBooking
        fields = ('nif', 'sex', 'tshirt_size', )
