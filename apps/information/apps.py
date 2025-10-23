from django.apps import AppConfig


class InformationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.information'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import load_seed_once
        post_migrate.connect(load_seed_once, sender=self)