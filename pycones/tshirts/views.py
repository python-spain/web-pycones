#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from pycones.tshirts.mixins import DisabledByOptionViewMixin
from .forms import TShirtForm, EntryForm
from .models import TshirtBooking


class TshirtBookingView(DisabledByOptionViewMixin, FormView):
    template_name = 'tshirts/show.html'

    # Default form class
    form_class = EntryForm

    # Default success_url
    success_url = reverse_lazy('tshirts:index')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        # check which form is loaded
        if self.get_form_class() == EntryForm:
            self.request.session['tshirt_authed'] = form.cleaned_data
            return response

        # Obtain the information of the entry we have to update
        session = self.request.session['tshirt_authed']

        # Don't continue unless the session is there
        if 'tshirt_authed' not in self.request.session:
            return response

        # Obtain the object
        obj = TshirtBooking.objects.get_or_create(
            email=session.get('email', ''),
            booking_id=session.get('booking_id', ''), )
        obj = obj[0]

        # Update it and save it
        obj.tshirt_size = form.cleaned_data['tshirt_size']
        obj.sex = form.cleaned_data['sex']
        obj.nif = form.cleaned_data['nif']
        obj.save()

        # Delete the session, we no longer need it
        del self.request.session['tshirt_authed']

        # Return the response
        return response

    def get_success_url(self):
        """ Change which success url is displayed depending if user is already authed by first form"""
        success_url = super().get_success_url()

        if self.get_form_class() == TShirtForm:
            success_url = reverse_lazy('tshirts:thanks')

        return success_url

    def get_form_class(self):
        """ Change which form is displayed depending if user is already authed by first form """
        form_class = super().get_form_class()

        # if session is there use TShirtForm
        if 'tshirt_authed' in self.request.session:
            form_class = TShirtForm

        return form_class


class Thanks(DisabledByOptionViewMixin, TemplateView):
    template_name = "tshirts/thanks.html"
