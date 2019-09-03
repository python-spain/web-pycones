#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class TshirtBooking(models.Model):
    # Tshirt choices
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'
    DOUBLE_EXTRA_LARGE = 'XXL'
    TSHIRT_CHOICES = [
        (SMALL, _('Pequeña')),
        (MEDIUM, _('Media')),
        (LARGE, _('Grande')),
        (EXTRA_LARGE, _('XL')),
        (DOUBLE_EXTRA_LARGE, _('XXL'))
    ]

    # Sex choices
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = [
        (MALE, _('Hombre')),
        (FEMALE, _('Mujer'))
    ]
    email = models.EmailField(max_length=120, )
    booking_id = models.CharField(max_length=120, )
    tshirt_size = models.CharField(_('Medida'), max_length=3, choices=TSHIRT_CHOICES, blank=True, )
    sex = models.CharField(_('Corte'), max_length=1, choices=SEX_CHOICES, blank=True, )
    nif = models.CharField(_('NIF/NIE'), max_length=9, help_text=_('Ingresa tu ID'), blank=True, )
    date_sent = models.DateTimeField(auto_now_add=True, null=True, blank=True, )

    def __str__(self):
        return '{email} - {booking_id}: {tshirt_size}, {sex}'.format(
            email=self.email,
            booking_id=self.booking_id,
            tshirt_size=self.tshirt_size,
            sex=self.sex, )

    class Meta:
        unique_together = ('email', 'booking_id')
