import datetime
import smtplib
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.utils import timezone

from sendflow.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingAttempt
from users.models import User


def get_next_scheduled_date(last_attempt_date, frequency):
    """Вычисляет следующую дату рассылки в зависимости от её периодичности."""
    if frequency == "D":
        return last_attempt_date + datetime.timedelta(days=1)
    elif frequency == "W":
        return last_attempt_date + datetime.timedelta(days=7)
    elif frequency == "M":
        return last_attempt_date + datetime.timedelta(days=30)
    return last_attempt_date


def get_mailings():
    """Собирает активные рассылки, готовые для отправки, и передает их на отправку."""
    mailing_client_dict = {}
    current_time = timezone.now()
    print("Текущее дата и время:", current_time)

    mailing_list = Mailing.objects.filter(is_published=True, status='W')

    for mailing in mailing_list:
        # Проверка последней успешной попытки рассылки
        last_attempt = MailingAttempt.objects.filter(mailing_id_id=mailing.id, status=True).order_by(
            'date_last_attempt').last()

        # Первая отправка или повторная проверка периодичности
        if last_attempt is None and mailing.date_of_first_dispatch <= current_time:
            mailing_client_dict[mailing] = mailing.client_list.all()
        elif last_attempt:
            next_date = get_next_scheduled_date(last_attempt.date_last_attempt, mailing.periodicity)
            if next_date <= current_time:
                mailing_client_dict[mailing] = mailing.client_list.all()

    do_send_mail(mailing_client_dict)


def do_send_mail(mailing_client_dict):
    """Отправляет сообщения клиентам из переданного словаря рассылок."""
    print("Количество рассылок для отправки:", len(mailing_client_dict))
    for mailing, client_list in mailing_client_dict.items():
        clients = [client.email for client in client_list]
        try:
            print(f'Отправка рассылки: {mailing.message_id.title}\n'
                  f'Сообщение: {mailing.message_id.message}\n'
                  f'Получатели: {clients}')
            server_response = send_mail(
                subject=mailing.message_id.title,
                message=mailing.message_id.message,
                from_email=EMAIL_HOST_USER,
                recipient_list=clients,
                fail_silently=False,
            )
            MailingAttempt.objects.create(status=True, server_response=server_response, mailing_id=mailing,
                                   owner=mailing.owner)
        except smtplib.SMTPException as error:
            MailingAttempt.objects.create(status=False, server_response=str(error), mailing_id=mailing, owner=mailing.owner)


def start():
    """Запускает планировщик для выполнения периодических задач."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_mailings, 'interval', seconds=10, id='mailing_scheduler_job')
    scheduler.start()
