# Generated by Django 4.2.2 on 2024-11-05 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
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
                ("title", models.CharField(max_length=250, verbose_name="Заголовок")),
                (
                    "summary",
                    models.CharField(max_length=250, verbose_name="Краткое содержание"),
                ),
                ("content", models.TextField(verbose_name="Текст статьи")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "views",
                    models.PositiveIntegerField(default=0, verbose_name="Просмотров"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Публикация"),
                ),
            ],
            options={
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
                "ordering": ("-created_at",),
            },
        ),
        migrations.DeleteModel(
            name="Blog",
        ),
    ]
