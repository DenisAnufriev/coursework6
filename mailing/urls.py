from django.urls import path

from mailing.views import (
    index,
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
    MailingDeleteView,
)

app_name = "mailing"

urlpatterns = [
    path("", index),
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/list/", ClientListView.as_view(), name="client_list"),
    path("client/view/<int:pk>/", ClientDetailView.as_view(), name="client_view"),
    path("client/edit/<int:pk>/", ClientUpdateView.as_view(), name="client_edit"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),

    path("letter/create/", LetterCreateView.as_view(), name="letter_create"),
    path("letter/list/", LetterListView.as_view(), name="letter_list"),
    path("letter/view/<int:pk>/", LetterDetailView.as_view(), name="letter_view"),
    path("letter/edit/<int:pk>/", LetterUpdateView.as_view(), name="letter_edit"),
    path("letter/delete/,<int:pk>/", LetterDeleteView.as_view(), name="letter_delete"),

    path("mail/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mail/list/", MailingListView.as_view(), name="mailing_list"),
    path("mail/view/<int:pk>/", MailingDetailView.as_view(), name="mailing_view"),
    path("mail/edit/<int:pk>/", MailingUpdateView.as_view(), name="mailing_edit"),
    path("mail/delete/,<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
]
