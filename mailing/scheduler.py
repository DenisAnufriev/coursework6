# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from apscheduler.jobstores.base import JobLookupError
# from mailing.tasks import send_mailing
#
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#
#     # Удалите существующую задачу, если она есть, чтобы избежать конфликта ID
#     try:
#         scheduler.remove_job('send_mailing_job')
#     except JobLookupError:
#         pass  # Если задача не найдена, продолжаем без ошибки
#
#     # Добавляем задачу заново
#     scheduler.add_job(send_mailing, 'interval', minutes=1, id='send_mailing_job')  # Запуск каждые 1 минуту
#     scheduler.start()