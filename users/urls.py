from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from users.views import UserCreateView, ProfileView


app_name = "users"

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    # path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    # path('reset_password/', reset_password, name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path(
    #     "toggle_active/<int:pk>/",
    #     UserToggleActiveView.as_view(),
    #     name="user_toggle_active",
    # ),
]
