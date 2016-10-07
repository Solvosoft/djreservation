from django.apps import AppConfig


class DjreservationConfig(AppConfig):
    name = 'djreservation'

    def ready(self):
        import djreservation.signals
        AppConfig.ready(self)