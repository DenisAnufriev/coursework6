import smtplib
from datetime import timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import Mailing, MailingAttempt


def check_and_send_mailings():
    """Проверяет и отправляет активные рассылки."""
    current_time = timezone.now()
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = current_time.astimezone(moscow_tz)

    print(f"Серверное время {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Текущее дата и время в Москве:", moscow_time.strftime('%Y-%m-%d %H:%M:%S'))

    # Получаем все активные и запланированные на отправку рассылки
    mailings = Mailing.objects.filter(
        is_active=True,
        send_time__lte=current_time,
        status=Mailing.Status.CREATED,
    )
    # print(f"существует {mailings}")
    for mailing in mailings:
        # print(f"mailing время отправки{mailing.send_time} текущее время {current_time} статус {mailing.status}")
        # print(mailing)
        if can_send_mailing(mailing):
            # print('отправка')
            send_mailing(mailing)


def can_send_mailing(mailing: Mailing) -> bool:
    """Проверяет, можно ли отправить рассылку на основе последней попытки."""
    # print('Проверяет, можно ли отправить рассылку на основе последней попытки.')
    last_attempt = MailingAttempt.objects.filter(
        mailing=mailing,
        status=MailingAttempt.Status.SUCCESS,
    ).order_by('-attempt_time').first()
    # if last_attempt:
    #     print(f'last_attempt mailing: {last_attempt.mailing}')
    # else:
    #     print('last_attempt is None')

    if not last_attempt:
        return True

    frequency_map = {
        Mailing.Frequency.DAILY: timedelta(days=1),
        Mailing.Frequency.WEEKLY: timedelta(weeks=1),
        Mailing.Frequency.MONTHLY: timedelta(days=30),
    }

    next_send_time = last_attempt.attempt_time + frequency_map[mailing.frequency]
    can_send = timezone.now() >= next_send_time

    return can_send


def send_mailing(mailing):
    clients = mailing.clients.all()
    emails = [client.email_client for client in clients]

    # Устанавливаем статус рассылки на "Запущена" перед отправкой
    attempt_status = MailingAttempt.Status.SUCCESS
    server_response = None
    print("send_mailing")
    try:
        mailing.status = Mailing.Status.RUNNING
        mailing.save()

        send_mail(
            subject=mailing.message.title,
            message=mailing.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
        )

        mailing.status = Mailing.Status.CREATED

        if mailing.frequency == Mailing.Frequency.DAILY:
            mailing.send_time += timedelta(days=1)
        elif mailing.frequency == Mailing.Frequency.WEEKLY:
            mailing.send_time += timedelta(weeks=1)
        elif mailing.frequency == Mailing.Frequency.MONTHLY:
            mailing.send_time += timedelta(days=30)

        mailing.save()

    except smtplib.SMTPException as error:
        mailing.is_active = False
        mailing.save()
        attempt_status = MailingAttempt.Status.FAILED
        server_response = str(error)

    finally:
        MailingAttempt.objects.create(
            mailing=mailing, status=attempt_status, server_response=server_response
        )
