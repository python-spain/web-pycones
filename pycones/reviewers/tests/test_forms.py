# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.contrib.auth.models import Group
from test_plus import TestCase

from pycones.proposals.tests.factories import ProposalFactory, ProposalKindFactory
from pycones.reviewers import REVIEW_GROUP_NAME
from pycones.reviewers.forms import ReviewForm
from pycones.reviewers.tests.factories import ReviewFactory
from pycones.users.tests.factories import UserFactory


class ReviewersFormsTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        group = Group.objects.get(name=REVIEW_GROUP_NAME)
        self.user.groups.add(group)

    def test_send_review(self):
        kind = ProposalKindFactory()
        proposal = ProposalFactory(kind=kind)
        review = ReviewFactory(proposal=proposal, user=self.user)
        data = {
            "score": 1.5
        }
        form = ReviewForm(instance=review, data=data)
        self.assertTrue(form.is_valid())
        review = form.save()
        self.assertAlmostEquals(review.score, data["score"])

    def test_send_review_round(self):
        kind = ProposalKindFactory()
        proposal = ProposalFactory(kind=kind)
        review = ReviewFactory(proposal=proposal, user=self.user)
        data = {
            "score": 1.67
        }
        form = ReviewForm(instance=review, data=data)
        self.assertTrue(form.is_valid())
        review = form.save()
        self.assertNotAlmostEqual(review.score, data["score"])

    def test_send_bad_review(self):
        kind = ProposalKindFactory()
        proposal = ProposalFactory(kind=kind)
        review = ReviewFactory(proposal=proposal, user=self.user)
        data = {
            "score": 5
        }
        form = ReviewForm(instance=review, data=data)
        self.assertFalse(form.is_valid())
