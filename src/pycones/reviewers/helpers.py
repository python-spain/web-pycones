# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.db import transaction
from django.db.utils import IntegrityError

from pycones.proposals.models import Proposal
from pycones.reviewers.models import Review


def create_reviews(user):
    """Create the reviews for the given user."""
    if user.reviews.count() != Proposal.objects.count():
        for proposal in Proposal.objects.iterator():
                try:
                    with transaction.atomic():
                        if not Review.objects.filter(user=user, proposal=proposal).exists():
                            Review.objects.create(user=user, proposal=proposal)
                except IntegrityError:
                    pass
