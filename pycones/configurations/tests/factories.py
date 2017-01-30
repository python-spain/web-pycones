# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import factory


class OptionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = "configurations.Option"
