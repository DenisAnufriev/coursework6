from django.urls import path

from mailing.views import index, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    LetterCreateView, LetterListView, LetterDetailView, LetterUpdateView, LetterDeleteView, MailCreateView, \
    MailListView, MailDetailView, MailUpdateView, MailDeleteView

app_name = 'mailing'

urlpatterns = [
    path('', index),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/view/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('letter/create/', LetterCreateView.as_view(), name='letter_create'),
    path('letter/list/', LetterListView.as_view(), name='letter_list'),
    path('letter/view/<int:pk>/', LetterDetailView.as_view(), name='letter_view'),
    path('letter/edit/<int:pk>/', LetterUpdateView.as_view(), name='letter_edit'),
    path('letter/delete/,<int:pk>/', LetterDeleteView.as_view(), name='letter_delete'),
    path('mail/create/', MailCreateView.as_view(), name='mail_create'),
    path('mail/list/', MailListView.as_view(), name='mail_list'),
    path('mail/view/<int:pk>/', MailDetailView.as_view(), name='mail_view'),
    path('mail/edit/<int:pk>/', MailUpdateView.as_view(), name='mail_edit'),
    path('mail/delete/,<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),

]
