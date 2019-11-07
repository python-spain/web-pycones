# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import factory


class ReviewFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = "reviewers.Review"
