# -*- coding: utf-8
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class NobinobiObservationConfig(AppConfig):
    name = 'nobinobi_observation'

    def ready(self):
        from nobinobi_observation.signals import create_group_nobinobi_observation, \
            create_group_admin_nobinobi_observation
        post_migrate.connect(create_group_nobinobi_observation, sender=self)
        post_migrate.connect(create_group_admin_nobinobi_observation, sender=self)
