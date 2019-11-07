# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions, register
from pycones.sponsorships.models import SponsorLevel


@register(SponsorLevel)
class SponsorLevelTranslationOptions(TranslationOptions):
    fields = ("name", "description")
