from django.apps import AppConfig


class MainwsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_contrib.environment_vars'

    verbose_name = 'django environment vars web app'
    author = 'Greg Flores'


