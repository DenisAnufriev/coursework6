from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView

from blog.models import Article
from mailing.forms import ClientForm, MailingForm, LetterForm
from mailing.models import Client, Letter, Mailing, MailingAttempt


@login_required
@permission_required('mailing.view_mailing')
def index(request):
    return render(request, 'mailing/index.html')


class HomePageView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Планировщик Рассылок"

        total_mailings = cache.get("total_mailings")
        if total_mailings is None:
            total_mailings = Mailing.objects.count()
        cache.set("total_mailings", total_mailings, 60 * 5)
        context["total_mailings"] = total_mailings

        active_mailings = cache.get("active_mailings")
        if active_mailings is None:
            active_mailings = Mailing.objects.filter(is_active=True).count()
        cache.set("active_mailings", active_mailings, 60 * 5)
        context["active_mailings"] = active_mailings

        unique_clients = cache.get("unique_clients")
        if unique_clients is None:
            unique_clients = Client.objects.distinct().count()
        cache.set("unique_clients", unique_clients, 60 * 5)
        context["unique_clients"] = unique_clients

        context["random_articles"] = Article.objects.order_by("?")[:3]
        return context


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    # fields = ('name', 'email_client')
    form_class = ClientForm
    permission_required = 'mailing.add_client'
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    # fields = ('name', 'email_client')
    form_class = ClientForm
    permission_required = 'mailing.change_client'
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'mailing.view_client'
    success_url = reverse_lazy('mailing:client_detail')


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'mailing.delete_client'
    success_url = reverse_lazy('mailing:client_list')


class LetterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Letter
    # fields = ('title', 'body')
    form_class = LetterForm
    permission_required = 'mailing.add_letter'
    success_url = reverse_lazy('mailing:letter_list')


class LetterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Letter
    # fields = ('title', 'body')
    form_class = LetterForm
    permission_required = 'mailing.change_letter'

    # success_url = reverse_lazy('mailing:letter_list')

    def get_success_url(self):
        return reverse('mailing:letter_detail', args=[self.kwargs.get('pk')])


class LetterListView(LoginRequiredMixin, ListView):
    model = Letter


class LetterDetailView(LoginRequiredMixin, DetailView):
    model = Letter


class LetterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Letter
    permission_required = 'mailing.delete_letter'
    success_url = reverse_lazy('mailing:letter_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    # fields = ('title', 'clients', 'message')
    form_class = MailingForm
    permission_required = 'mailing.add_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    # fields = ('title', 'clients', 'message')
    form_class = MailingForm
    permission_required = 'mailing.change_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Планировщик Рассылок"

        total_mailings = Mailing.objects.count()
        context["total_mailings"] = total_mailings

        active_mailings = Mailing.objects.filter(is_active=True).count()
        context["active_mailings"] = active_mailings

        unique_clients = Client.objects.distinct().count()
        context["unique_clients"] = unique_clients

        # context["random_articles"] = Article.objects.order_by("?")[:3]
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingAttemptListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingAttempt
    permission_required = 'mailing.view_attempt'
    context_object_name = 'mailing_attempts'
    template_name = 'mailing/mailing_attempt_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Общая статистика рассылок
        context['total_mailings'] = Mailing.objects.count()
        context['successful_attempts'] = MailingAttempt.objects.filter(status=MailingAttempt.Status.SUCCESS).count()
        context['failed_attempts'] = MailingAttempt.objects.filter(status=MailingAttempt.Status.FAILED).count()

        return context


class MailingAttemptDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingAttempt
    permission_required = 'mailing.view_attempt'
    context_object_name = 'mailing_attempt'  # имя переменной для доступа в шаблоне
    template_name = 'mailing/mailing_attempt_detail.html'


# class MailingAttemptCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = MailingAttempt
#     permission_required = 'mailing.create_attempt'
#
#     def form_valid(self, form):
#         # attempt = form.save()
#         # user = self.request.user
#         # attempt.owner = user
#         # attempt.save()
#         form.instance.owner = self.request.user  # так исключается одно обращение к базе
#         return super().form_valid(form)


@login_required
@permission_required('mailing.view_mailing')
def toggle_activity(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.is_active:
        mailing.is_active = False
    else:
        mailing.is_active = True

    mailing.save()
    return redirect(reverse('mailing:index'))
