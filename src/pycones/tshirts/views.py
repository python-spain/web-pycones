
from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import UpdateView
from django.utils.translation import ugettext_lazy as _

from pycones.tshirts.mixins import DisabledByOptionViewMixin
from pycones.tshirts.forms import TShirtForm, EntryForm
from pycones.tshirts.models import TshirtBooking


class Tshirt(DisabledByOptionViewMixin, FormView):
    form_class = EntryForm
    template_name = 'tshirts/forms/validate.html'
    success_url = reverse_lazy('tshirts:update')

    def form_valid(self, form):
        response = super().form_valid(form)

        # if form is valid pass data from it to session
        session = self.request.session['tshirt_authed'] = form.cleaned_data
        return response


class TshirtUpdate(DisabledByOptionViewMixin, UpdateView):
    form_class = TShirtForm
    template_name = 'tshirts/forms/tshirtbooking_update.html'
    success_url = reverse_lazy('tshirts:thanks')

    def get_object(self, queryset=None):

        # if session exists, set object to populate with data from session
        if self.request.session.keys():
            session = self.request.session['tshirt_authed']
            obj = TshirtBooking.objects.get_or_create(
                email=session['email'],
                booking_id=session['booking_id'], )
            obj = obj[0]
        else:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.keys():
            session = self.request.session['tshirt_authed']
            obj = TshirtBooking.objects.get_or_create(
                email=session['email'],
                booking_id=session['booking_id'], )
            obj = obj[0]

            # if NIF field is not empty show a message informing about editing entry
            if obj.nif is not '':
                messages.add_message(self.request, messages.INFO, _('Estás editando tu entrada'))

        return context

    def form_valid(self, form):
        valid = super().form_valid(form)
        self.request.session.flush()
        return valid


class Thanks(DisabledByOptionViewMixin, TemplateView):
    template_name = "tshirts/thanks.html"
