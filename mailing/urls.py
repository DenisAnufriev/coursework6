from django.urls import path

from mailing.views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClientDeleteView,
    LetterCreateView,
    LetterListView,
    LetterDetailView,
    LetterUpdateView,
    LetterDeleteView,
    MailingCreateView,
    MailingListView,
    MailingDetailView,
    MailingUpdateView,
    MailingDeleteView, MailingAttemptListView, MailingAttemptDetailView, HomePageView, MailingToggleActiveView,
)

app_name = "mailing"

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/list/", ClientListView.as_view(), name="client_list"),
    path("client/view/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/edit/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),

    path("letter/create/", LetterCreateView.as_view(), name="letter_create"),
    path("letter/list/", LetterListView.as_view(), name="letter_list"),
    path("letter/view/<int:pk>/", LetterDetailView.as_view(), name="letter_detail"),
    path("letter/edit/<int:pk>/", LetterUpdateView.as_view(), name="letter_update"),
    path("letter/delete/<int:pk>/", LetterDeleteView.as_view(), name="letter_delete"),

    path("mail/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mail/list/", MailingListView.as_view(), name="mailing_list"),
    path("mail/view/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mail/edit/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mail/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path(
        "toggle-active/<int:pk>/",
        MailingToggleActiveView.as_view(),
        name="mailing_toggle_active",
    ),

    path("mailingattempt/list/", MailingAttemptListView.as_view(), name="mailing_attempt_list"),
    path("mailingattempt/view/<int:pk>/", MailingAttemptDetailView.as_view(), name="mailing_attempt_detail"),
]
