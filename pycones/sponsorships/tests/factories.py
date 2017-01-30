# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import factory

from pycones.users.tests.factories import UserFactory


class SponsorLevelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = "sponsorships.SponsorLevel"


class SponsorFactory(factory.django.DjangoModelFactory):

    applicant = factory.SubFactory(UserFactory)
    level = factory.SubFactory(SponsorLevelFactory)

    class Meta:
        model = "sponsorships.Sponsor"
