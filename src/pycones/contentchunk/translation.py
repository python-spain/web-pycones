# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions, translator

from .models import Chunk


class ChunkTranslationOptions(TranslationOptions):
    fields = ("text",)


translator.register(Chunk, ChunkTranslationOptions)
