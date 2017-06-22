# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation.translator import TranslationOptions, translator

from pycones.proposals.models import ProposalKind, Proposal


class ProposalKindTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')


class ProposalTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'additional_notes', 'description', )


translator.register(ProposalKind, ProposalKindTranslationOptions)
translator.register(Proposal, ProposalTranslationOptions)
