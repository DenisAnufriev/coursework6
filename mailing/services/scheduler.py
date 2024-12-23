from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from mailing.services.mailing_servise import check_and_send_mailings

# Создаём объект планировщика
scheduler = BackgroundScheduler()


def start_scheduler():
    """Запускает планировщик для выполнения периодических задач."""
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Удаляем существующую задачу, чтобы избежать конфликта ID
    job_id = 'send_mailing_job'
    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        print(f"Задача с ID {job_id} не найдена. Создаём новую.")

    # Добавляем задачу с интервалом в 60 секунд
    scheduler.add_job(
        check_and_send_mailings,
        'interval',
        seconds=60,
        id=job_id,
        replace_existing=True  # Обеспечивает замену существующей задачи
    )

    scheduler.start()
    print("Планировщик запущен.")


# Остановка планировщика при необходимости
def stop_scheduler():
    """Останавливает планировщик."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Планировщик остановлен.")

# from apscheduler.jobstores.base import JobLookupError
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
#
# from mailing.services.mailing_servise import check_and_send_mailings
#
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
#     scheduler.add_job(check_and_send_mailings, 'interval', seconds=60, id='send_mailing_job')  # Запуск каждые 1 минуту
#     scheduler.start()
#     print("scheduler start")


# def start_scheduler():
#     """Запускает планировщик для выполнения периодических задач."""
#     global scheduler
#     if scheduler is None:
#         scheduler = BackgroundScheduler()
#         scheduler.add_job(check_and_send_mailings, 'interval', seconds=60, id='mailing_scheduler_job')
#         scheduler.start()
#         print("scheduler start")
