#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class TshirtBooking(models.Model):
    """ Model where tshirt details for the different guests are saved """

    # TShirt choices
    TSHIRT_CHOICE_S = 'S'
    TSHIRT_CHOICE_M = 'M'
    TSHIRT_CHOICE_L = 'L'
    TSHIRT_CHOICE_XL = 'XL'
    TSHIRT_CHOICE_XXL = 'XXL'
    TSHIRT_CHOICE_XXXL = 'XXXL'
    TSHIRT_CHOICES = (
        (TSHIRT_CHOICE_S, _('S')),
        (TSHIRT_CHOICE_M, _('M')),
        (TSHIRT_CHOICE_L, _('L')),
        (TSHIRT_CHOICE_XL, _('XL')),
        (TSHIRT_CHOICE_XXL, _('XXL')),
        (TSHIRT_CHOICE_XXXL, _('XXXL')), )

    # Sex choices
    SEX_CHOICE_MALE = 'M'
    SEX_CHOICE_FEMALE = 'F'
    SEX_CHOICES = (
        (SEX_CHOICE_MALE, _('Hombre')),
        (SEX_CHOICE_FEMALE, _('Mujer')), )

    # Guests
    email = models.EmailField(max_length=120, )
    booking_id = models.CharField(max_length=120, )
    nif = models.CharField(_('NIF/NIE'), max_length=9, help_text=_('Ingresa tu NIF/NIE'), blank=True, )

    # Shirt
    tshirt_size = models.CharField(_('Medida'), max_length=3, choices=TSHIRT_CHOICES, blank=True, )
    sex = models.CharField(_('Corte'), max_length=1, choices=SEX_CHOICES, blank=True, )

    # Other
    date_sent = models.DateTimeField(auto_now_add=True, null=True, blank=True, )

    def __str__(self):
        return '{email} - {booking_id}: {tshirt_size}, {sex}'.format(
            email=self.email,
            booking_id=self.booking_id,
            tshirt_size=self.tshirt_size,
            sex=self.sex, )

    class Meta:
        unique_together = ('email', 'booking_id')
