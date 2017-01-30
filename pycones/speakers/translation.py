# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import TranslationOptions, translator

from speakers.models import Speaker


class SpeakerTranslationOptions(TranslationOptions):
    fields = ('biography', )

translator.register(Speaker, SpeakerTranslationOptions)
