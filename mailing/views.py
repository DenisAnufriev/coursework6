from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing.forms import ClientForm, MailForm, LetterForm
from mailing.models import Client, Letter, Mail


def index(request):
    return render(request, 'mailing/index.html')

class ClientCreateView(CreateView):
    model = Client
    # fields = ('name', 'email_client')
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    # fields = ('name', 'email_client')
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class LetterCreateView(CreateView):
    model = Letter
    # fields = ('title', 'body')
    form_class = LetterForm
    success_url = reverse_lazy('mailing:letter_list')


class LetterUpdateView(UpdateView):
    model = Letter
    # fields = ('title', 'body')
    form_class = LetterForm
    success_url = reverse_lazy('mailing:letter_list')

    def get_success_url(self):
        return reverse('mailing:letter_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        LetterFormset = inlineformset_factory(Letter, )


class LetterListView(ListView):
    model = Letter


class LetterDetailView(DetailView):
    model = Letter


class LetterDeleteView(DeleteView):
    model = Letter
    success_url = reverse_lazy('mailing:letter_list')


class MailCreateView(CreateView):
    model = Mail
    # fields = ('title', 'clients', 'message')
    form_class = MailForm
    success_url = reverse_lazy('mailing:mail_list')


class MailUpdateView(UpdateView):
    model = Mail
    # fields = ('title', 'clients', 'message')
    form_class = MailForm
    success_url = reverse_lazy('mailing:mail_list')


class MailListView(ListView):
    model = Mail


class MailDetailView(DetailView):
    model = Mail


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('mailing:mail_list')