# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import TranslationOptions, translator

from blog.models import Post


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'content')
    fallback_languages = {'default': ('es', 'en', 'ca')}


translator.register(Post, PostTranslationOptions)
