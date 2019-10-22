# -*- coding: utf-8 -*-

from modeltranslation.translator import TranslationOptions, translator

from pycones.blog.models import Post


class PostTranslationOptions(TranslationOptions):
    fields = ("title", "slug", "content")
    fallback_languages = {"default": ("es", "en", "ca")}


translator.register(Post, PostTranslationOptions)
