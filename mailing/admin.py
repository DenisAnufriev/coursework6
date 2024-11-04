from django.contrib import admin

from mailing.models import Client, Letter, Mailing, MailingAttempt


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_client', 'full_name', 'comment',)
    list_filter = ('email_client',)
    search_fields = ('email_client',)


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'message', 'created_at', 'update_at', 'owner',)
    list_filter = ('created_at', 'update_at',)
    search_fields = ('title', 'message',)


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


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_time", "mailing", "status", "server_response",)
    list_filter = ("id",)
    # search_fields = ("id", "attempt_time", "mailing", "status",)
