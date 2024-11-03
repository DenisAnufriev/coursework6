from django.forms import ModelForm

from mailing.models import Client, Letter, Mail


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        # exclude = ("email_client",)

class LetterForm(ModelForm):
    class Meta:
        model = Letter
        fields = "__all__"
        # exclude = ("email_client",)

class MailForm(ModelForm):
    class Meta:
        model = Mail
        fields = "__all__"
        # exclude = ("email_client",)

