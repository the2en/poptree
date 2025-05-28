from django.apps import AppConfig

class SpendingConfig(AppConfig):
    name = 'spending'

    def ready(self):
        import spending.signals
