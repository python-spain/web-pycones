# -*- coding: utf-8 -*-

from modeltranslation.translator import TranslationOptions, translator

from pycones.speakers.models import Speaker


class SpeakerTranslationOptions(TranslationOptions):
    fields = ("biography",)


translator.register(Speaker, SpeakerTranslationOptions)
