from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_migrate


class SpeakersConfig(AppConfig):
    name = "pycones.speakers"

    def ready(self):
        from pycones.speakers.signals import register_speakers_handler
        from pycones.speakers.signals import create_speakers_group

        user_model = get_user_model()
        m2m_changed.connect(register_speakers_handler, sender=user_model.groups.through)
        post_migrate.connect(create_speakers_group)
