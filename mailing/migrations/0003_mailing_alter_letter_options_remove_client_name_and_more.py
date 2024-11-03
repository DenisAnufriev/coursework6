# Generated by Django 4.2.2 on 2024-11-03 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mailing", "0002_rename_clienty_mail_clients"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="активность рассылки"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата и время создания рассылки"
                    ),
                ),
                (
                    "send_time",
                    models.DateTimeField(verbose_name="дата и время отправки рассылки"),
                ),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("D", "Раз в день"),
                            ("W", "Раз в неделю"),
                            ("M", "Раз в месяц"),
                        ],
                        default="W",
                        max_length=1,
                        verbose_name="периодичность",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("CR", "Создана"), ("RN", "Запущена")],
                        default="CR",
                        max_length=2,
                        verbose_name="статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
                "ordering": ("-created_at",),
                "permissions": [
                    ("disable_mailing", "Может делать рассылку неактивной")
                ],
            },
        ),
        migrations.AlterModelOptions(
            name="letter",
            options={
                "ordering": ("title",),
                "verbose_name": "сообщение",
                "verbose_name_plural": "сообщения",
            },
        ),
        migrations.RemoveField(
            model_name="client",
            name="name",
        ),
        migrations.AddField(
            model_name="client",
            name="full_name",
            field=models.CharField(
                blank=True,
                help_text="(при наличии)",
                max_length=100,
                null=True,
                verbose_name="ФИО",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец клиента",
            ),
        ),
        migrations.AddField(
            model_name="letter",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец сообщения",
            ),
        ),
        migrations.DeleteModel(
            name="Mail",
        ),
        migrations.AddField(
            model_name="mailing",
            name="clients",
            field=models.ManyToManyField(
                related_name="clients", to="mailing.client", verbose_name="клиенты"
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mailings",
                to="mailing.letter",
                verbose_name="сообщения",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец рассылки",
            ),
        ),
    ]
