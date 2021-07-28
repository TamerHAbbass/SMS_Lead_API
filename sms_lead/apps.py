from django.apps import AppConfig


class SmsLeadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms_lead'

    def ready(self):
        from .sms_run import main
        main()