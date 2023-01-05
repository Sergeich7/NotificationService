from django.apps import AppConfig


class NotifyConfig(AppConfig):
    name = 'notify'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Рассылки'

    def ready(self):
        import notify.signals

