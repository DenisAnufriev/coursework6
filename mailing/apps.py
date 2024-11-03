from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        from mailing.services.scheduler import start_scheduler
        try:
            start_scheduler()
        except Exception as e:
            print(f"Ошибка при запуске планировщика: {e}")
