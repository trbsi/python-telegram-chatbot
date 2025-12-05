from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.authentication'

    def ready(self):
        import src.authentication.signals
