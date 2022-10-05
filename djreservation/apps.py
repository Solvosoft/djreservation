from django.apps import AppConfig


class DjreservationConfig(AppConfig):
    name = 'djreservation'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import djreservation.signals
        AppConfig.ready(self)