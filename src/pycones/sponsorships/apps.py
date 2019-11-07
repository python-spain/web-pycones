# -*- coding: utf-8 -*-


from django.apps import AppConfig
from django.db.models.signals import post_init, post_save


def _store_initial_level(sender, instance, **kwargs):
    if instance:
        instance._initial_level_id = instance.level_id


def _check_level_change(sender, instance, created, **kwargs):
    if instance and (created or instance.level_id != instance._initial_level_id):
        instance.reset_benefits()


class SponsorshipConfig(AppConfig):
    name = "pycones.sponsorships"

    def ready(self):
        """Connects signals with their managers."""
        from pycones.sponsorships.models import Sponsor

        post_init.connect(_store_initial_level, sender=Sponsor)
        post_save.connect(_check_level_change, sender=Sponsor)
