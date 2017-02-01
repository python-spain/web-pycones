# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from test_plus import TestCase

from pycones.proposals import BASIC_LEVEL, ABSTRACT_MINIMUM_WORDS
from pycones.proposals.forms import ProposalFrom
from pycones.proposals.models import Proposal
from pycones.proposals.tests.factories import ProposalKindFactory


class ProposalFromTest(TestCase):

    def setUp(self):
        self.kinds = ProposalKindFactory.create_batch(size=2)

    def test_post_proposal(self):
        data = {
            "kind": self.kinds[0].id,
            "audience_level": BASIC_LEVEL,
            "title": "foo",
            "description": "bar",
            "abstract": "bla " * ABSTRACT_MINIMUM_WORDS,
            "additional_notes": "",
            "language": "es"
        }
        form = ProposalFrom(data)
        self.assertTrue(form.is_valid())

    def test_post_proposal_bad_abstract(self):
        data = {
            "kind": self.kinds[0].id,
            "audience_level": BASIC_LEVEL,
            "title": "foo",
            "description": "bar",
            "abstract": "bla",
            "additional_notes": "",
            "language": "es"
        }
        form = ProposalFrom(data)
        self.assertFalse(form.is_valid())
        data = {
            "kind": self.kinds[0].id,
            "audience_level": BASIC_LEVEL,
            "title": "foo",
            "description": "bar",
            "abstract": "",
            "additional_notes": "",
            "language": "es"
        }
        form = ProposalFrom(data)
        self.assertFalse(form.is_valid())

    def test_post_proposal_and_notify(self):
        data = {
            "kind": self.kinds[0].id,
            "audience_level": BASIC_LEVEL,
            "title": "foo",
            "description": "bar",
            "abstract": "bla " * ABSTRACT_MINIMUM_WORDS,
            "additional_notes": "",
            "language": "es"
        }
        form = ProposalFrom(data)
        self.assertTrue(form.is_valid())
        proposal = form.save()
        self.assertIsInstance(proposal, Proposal)
        self.assertTrue(proposal.notified)
