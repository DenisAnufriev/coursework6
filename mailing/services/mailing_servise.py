from mailing.models import Mailing, MailingJob
from django.utils import timezone
from datetime import timedelta
import smtplib
from django.core.mail import send_mail
from django.conf import settings


def check_and_send_mailings():
    current_time = timezone.now()

    # Фильтруем рассылки, которые можно отправлять
    mailings = Mailing.objects.filter(
        status=Mailing.Status.CREATED, send_time__lte=current_time, is_active=True,
    )

    for mailing in mailings:
        if can_send_mailing(mailing):
            send_mailing(mailing)


def can_send_mailing(mailing: Mailing) -> bool:
    # Проверяем последнюю попытку отправки
    last_attempt = (
        MailingJob.objects.filter(
            mailing=mailing, status=MailingJob.Status.SUCCESS
        )
        .order_by("-attempt_time")
        .first()
    )

    # Если еще не было попыток отправки, то можно отправлять
    if not last_attempt:
        return True

    # Определяем время следующей отправки
    frequency_map = {
        Mailing.Frequency.DAILY: timedelta(days=1),
        Mailing.Frequency.WEEKLY: timedelta(weeks=1),
        Mailing.Frequency.MONTHLY: timedelta(days=30),
    }
    next_send_time = last_attempt.attempt_time + frequency_map[mailing.frequency]

    return timezone.now() >= next_send_time


def send_mailing(mailing: Mailing):
    clients = mailing.clients.all()
    emails = [client.email_client for client in clients]  # Исправлено на email_client

    attempt_status = MailingJob.Status.SUCCESS
    server_response = None

    try:
        mailing.status = Mailing.Status.RUNNING
        mailing.save()

        # Отправляем письмо
        send_mail(
            subject=mailing.message.title,
            message=mailing.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
        )

        # Обновляем статус и время следующей отправки
        mailing.status = Mailing.Status.CREATED
        update_next_send_time(mailing)

        mailing.save()

    except smtplib.SMTPException as error:
        mailing.is_active = False
        mailing.save()
        attempt_status = MailingJob.Status.FAILED
        server_response = str(error)

    finally:
        MailingJob.objects.create(
            mailing=mailing, status=attempt_status, server_response=server_response
        )


def update_next_send_time(mailing: Mailing):
    """Обновляем время следующей отправки для рассылки в зависимости от её частоты."""
    if mailing.frequency == Mailing.Frequency.DAILY:
        mailing.send_time += timedelta(days=1)
    elif mailing.frequency == Mailing.Frequency.WEEKLY:
        mailing.send_time += timedelta(weeks=1)
    elif mailing.frequency == Mailing.Frequency.MONTHLY:
        mailing.send_time += timedelta(days=30)
