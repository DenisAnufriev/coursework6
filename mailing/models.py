from django.db import models


from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    """Клиенты для рассылок"""
    full_name = models.CharField(
        max_length=100,
        verbose_name="ФИО",
        help_text="Обязательно",
    )
    email_client = models.EmailField(
        verbose_name="электронная почта",
        help_text="Обязательно",
    )
    comment = models.TextField(
        verbose_name="Комментарий", help_text="Добавьте комментарий", **NULLABLE
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
        ordering = ("full_name",)


class Letter(models.Model):
    """Письма для рассылок"""
    title = models.CharField(
        max_length=100,
        default="Рассылка",
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    message = models.TextField(verbose_name="Сообщение", help_text="Введите текс")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    owner = models.ForeignKey(
        User,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Введите владельца",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ("title",)


class Mailing(models.Model):
    """Рассылки"""
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
        **NULLABLE,
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
        return (f"ID: {self.id},"
                f" Статус: {self.get_status_display()}")

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ("-created_at",)
        permissions = [
            ("disable_mailing", "Может делать рассылку неактивной"),
        ]


class MailingAttempt(models.Model):
    """Представляет собой попытку отправить почтовое сообщение."""

    class Status(models.TextChoices):
        SUCCESS = "SC", "Успешно"
        FAILED = "FL", "Неуспешно"

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="рассылка",
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время попытки отправки"
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, verbose_name="статус попытки"
    )
    server_response = models.TextField(
        verbose_name="ответ почтового сервера", **NULLABLE
    )

    def __str__(self):
        return f"Рассылка создана: {self.mailing}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
        ordering = ["-attempt_time"]
