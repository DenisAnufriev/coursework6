from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя, наследующая функционал UserCreationForm
    и применяющая стиль из StyleFormMixin.
    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name",)


    # def __init__(self, *args, **kwargs):
    #     """
    #     Инициализация формы, скрывающая поле для пароля.
    #
    #     :param args: Позиционные аргументы.
    #     :param kwargs: Именованные аргументы.
    #     """
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields["password"].widget = forms.HiddenInput()