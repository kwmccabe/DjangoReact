from django.apps import AppConfig


# see settings.py INSTALLED_APPS
class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
