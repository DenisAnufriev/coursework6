from django.core.mail import send_mail
from django.utils import timezone
from .models import Mailing, MailingAttempt
from django.conf import settings  # Импортируем настройки Django


def send_mailing():
    # Получите активные рассылки, которые необходимо отправить
    mailings = Mailing.objects.filter(
        is_active=True,
        send_time__lte=timezone.now(),
        status=Mailing.Status.RUNNING
    )

    for mailing in mailings:
        # Подготовка списка адресов для отправки
        client_emails = mailing.clients.values_list('email_client', flat=True)

        # Отправка писем
        for email in client_emails:
            try:
                send_mail(
                    mailing.message.title,
                    mailing.message.message,
                    settings.DEFAULT_FROM_EMAIL,  # Используем DEFAULT_FROM_EMAIL
                    [email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.Status.SUCCESS,
                    server_response='Mail sent successfully'
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.Status.FAILED,
                    server_response=str(e)
                )
