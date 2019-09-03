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

    def form_valid(self, form):
        response = super().form_valid(form)

        # check which form is loaded
        if self.get_form_class() == EntryForm:
            self.request.session['tshirt_authed'] = form.cleaned_data
            return response

        session = self.request.session['tshirt_authed']
        obj = TshirtBooking.objects.get_or_create(
            email=session['email'],
            booking_id=session['booking_id'], )
        obj = obj[0]

        obj.tshirt_size = form.cleaned_data['tshirt_size']
        obj.sex = form.cleaned_data['sex']
        obj.nif = form.cleaned_data['nif']

        obj.save()

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
