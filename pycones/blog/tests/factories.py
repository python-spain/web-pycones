# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import factory
from factory.fuzzy import FuzzyText


class PostFactory(factory.django.DjangoModelFactory):

    title = FuzzyText()

    class Meta:
        model = "blog.Post"
