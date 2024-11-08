# from time import sleep
import os
import sys

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        if "runserver" in sys.argv and os.environ.get("RUN_MAIN") == "true":
            from mailing.services.scheduler import start_scheduler

            start_scheduler()

    # def ready(self):
    #     """ Метод для автоматического запуска рассылки """
    #     from mailing.services import start
    #
    #     sleep(10)
    #     start()
