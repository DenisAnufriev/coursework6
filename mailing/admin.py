from django.contrib import admin

from mailing.models import Client, Letter, Mailing, MailingJob


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email_client', 'full_name',)
    list_filter = ('email_client',)
    search_fields = ('email_client',)


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('title', 'body',)
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "is_active",
        "send_time",
        "frequency",
    )
    list_filter = ("owner",)
    search_fields = ("owner", "send_time", "id", "is_active",)

@admin.register(MailingJob)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id",)
