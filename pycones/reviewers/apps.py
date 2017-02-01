from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_migrate


class ReviewersConfig(AppConfig):
    name = "pycones.reviewers"

    def ready(self):
        from pycones.reviewers.signals import register_reviews_handler
        from pycones.reviewers.signals import create_reviewers_group

        user_model = get_user_model()
        m2m_changed.connect(register_reviews_handler, sender=user_model.groups.through)
        post_migrate.connect(create_reviewers_group)
