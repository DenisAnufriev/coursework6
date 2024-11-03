from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    full_name = models.CharField(
        max_length=100,
        verbose_name="ФИО",
        help_text="при наличии",
        **NULLABLE,
    )
    email_client = models.EmailField(
        verbose_name="электронная почта",
        help_text="обязательно",
        unique=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="владелец клиента",
    )

    def __str__(self):
        return f"{self.email_client} ({self.full_name})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ("email_client",)


class Letter(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Тема письма",
    )
    body = models.TextField(verbose_name="содержимое")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="владелец сообщения",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ("title",)


class Mailing(models.Model):
    class Status(models.TextChoices):
        CREATED = "CR", "Создана"
        RUNNING = "RN", "Запущена"

    class Frequency(models.TextChoices):
        DAILY = "D", "Раз в день"
        WEEKLY = "W", "Раз в неделю"
        MONTHLY = "M", "Раз в месяц"

    is_active = models.BooleanField(default=True, verbose_name="активность рассылки")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время создания рассылки"
    )
    send_time = models.DateTimeField(verbose_name="дата и время отправки рассылки")
    frequency = models.CharField(
        max_length=1,
        choices=Frequency.choices,
        default=Frequency.WEEKLY,
        verbose_name="периодичность",
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="статус",
    )
    message = models.ForeignKey(
        Letter,
        on_delete=models.PROTECT,
        related_name="mailings",
        verbose_name="сообщения",
    )
    clients = models.ManyToManyField(
        Client,
        related_name="clients",
        verbose_name="клиенты",
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="владелец рассылки",
    )

    def __str__(self):
        return f"Рассылка: {self.id}, Статус: {self.get_status_display()}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ("-created_at",)
        permissions = [
            ("disable_mailing", "Может делать рассылку неактивной"),
        ]


class MailingJob(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "SC", "Успешно"
        FAILED = "FL", "Неуспешно"

    id = models.AutoField(primary_key=True)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name='jobs', verbose_name='рассылка'
    )
    job_id = models.CharField(max_length=255, unique=True)
    next_run_time = models.DateTimeField(**NULLABLE)
    trigger = models.CharField(max_length=50)
    args = models.JSONField(**NULLABLE)
    kwargs = models.JSONField(**NULLABLE)
    job_state = models.JSONField(**NULLABLE)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.SUCCESS,
        verbose_name="статус попытки"
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="время попытки"
    )
    server_response = models.TextField(
        verbose_name="ответ почтового сервера", **NULLABLE
    )

    def __str__(self):
        return f"Job for '{self.mailing}' with ID: {self.job_id}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
        ordering = ["-mailing"]
