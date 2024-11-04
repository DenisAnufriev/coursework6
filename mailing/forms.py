from django.forms import ModelForm, BooleanField, DateTimeInput

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
        fields = "__all__"
        # exclude = ("email_client",)


class LetterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Letter
        fields = "__all__"
        # exclude = ("email_client",)


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        # fields = "__all__"
        exclude = ('owner',)
        # widgets = {
        #     'send_time': DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime.local'}),
        # }
