from django.forms.models import ModelForm
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _
from pycones.tshirts.models import TshirtBooking


class EntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-2 input-lg'})
        self.fields['booking_id'].widget.attrs.update({'class': "form-control mb-5 input-lg"})

    def clean(self):
        cleaned_data = self.cleaned_data
        clean_email = cleaned_data['email']
        clean_booking_id = cleaned_data['booking_id']
        check = TshirtBooking.objects.filter(email=clean_email, booking_id=clean_booking_id).exists()
        if not check:
            self.add_error(None, _('Your data is invalid.'))
        return cleaned_data

    class Meta:
        model = TshirtBooking
        fields = ['email', 'booking_id']


class TShirtForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nif'].widget.attrs.update({'class': 'form-control mb-2 input-lg'})
        self.fields['sex'].widget.attrs.update({'class': 'form-control mb-5 input-lg'})
        self.fields['tshirt_size'].widget.attrs.update({'class': 'form-control mb-5 input-lg'})

    class Meta:
        model = TshirtBooking
        fields = ['nif', 'sex', 'tshirt_size']
        widgets = {
            'tshirt_size': Select(),
            'sex': Select(),
        }
