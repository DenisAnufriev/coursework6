# Generated by Django 4.2.2 on 2024-11-03 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mailing", "0001_initial"),
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="mailing.client",
                verbose_name="Клиент",
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="mailing",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="mailing.mailing",
                verbose_name="Рассылки",
            ),
        ),
    ]
