from django.forms import ModelForm, BooleanField, DateTimeInput
from django import forms
from mailing.models import Client, Letter, Mailing


class StyleFormMixin:
    """
    Миксин для установки стилей для полей форм.

    При инициализации добавляет классы CSS к полям формы:
    - 'form-check-input' для полей типа BooleanField
    - 'form-control' для остальных полей
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (
                field_name,
                field,
        ) in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        # fields = "__all__"
        exclude = ("owner",)


class LetterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Letter
        fields = ('title', 'message',)
        # exclude = ("email_client",)


class MailingForm(StyleFormMixin, forms.ModelForm):
    send_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
        label="Дата и время первой отправки рассылки",
    )

    class Meta:
        model = Mailing
        fields = [
            "is_active",
            "send_time",
            "frequency",
            "message",
            "clients",
        ]
