import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing:client_detail", kwargs={"pk": self.object.pk})


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    # fields = ('name', 'email_client')
    form_class = ClientForm
    permission_required = 'mailing.change_client'
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    ordering = ("-id",)
    permission_required = "mailing.view_client"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(owner=user)


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
    # fields = ('title', 'message')
    form_class = LetterForm
    permission_required = 'mailing.add_letter'

    # success_url = reverse_lazy('mailing:letter_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing:letter_detail", kwargs={"pk": self.object.pk})


class LetterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Letter
    # fields = ('title', 'message')
    form_class = LetterForm
    permission_required = 'mailing.change_letter'


    def get_success_url(self):
        return reverse_lazy('mailing:letter_detail', args=[self.kwargs.get('pk')])


class LetterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Letter
    permission_required = "mailing.view_letter"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Letter.objects.all()
        return Letter.objects.filter(owner=user)


class LetterDetailView(LoginRequiredMixin, DetailView):
    model = Letter
    permission_required = "mailing.view_letter"


class LetterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Letter
    success_url = reverse_lazy('mailing:letter_list')
    permission_required = 'mailing.delete_letter'


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    # fields = ('title', 'clients', 'message')
    form_class = MailingForm
    permission_required = 'mailing.add_mailing'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    # fields = ('title', 'clients', 'message')
    form_class = MailingForm
    permission_required = 'mailing.change_mailing'

    # success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = "mailing.view_mailing"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список рассылок"
        return context


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    permission_required = "mailing.view_mailing"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    # permission_required = 'mailing.view_attempt'
    context_object_name = 'mailing_attempts'
    template_name = 'mailing/mailing_attempt_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Общая статистика рассылок
        context['total_mailings'] = Mailing.objects.count()
        context['successful_attempts'] = MailingAttempt.objects.filter(status=MailingAttempt.Status.SUCCESS).count()
        context['failed_attempts'] = MailingAttempt.objects.filter(status=MailingAttempt.Status.FAILED).count()

        return context


class MailingAttemptDetailView(LoginRequiredMixin, DetailView):
    model = MailingAttempt
    # permission_required = 'mailing.view_attempt'
    context_object_name = 'mailing_attempt'  # имя переменной для доступа в шаблоне
    template_name = 'mailing/mailing_attempt_detail.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


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


# @login_required
# @permission_required('mailing.view_mailing')
# def toggle_activity(request, pk):
#     mailing = get_object_or_404(Mailing, pk=pk)
#     if mailing.is_active:
#         mailing.is_active = False
#     else:
#         mailing.is_active = True
#
#     mailing.save()
#     return redirect(reverse('mailing:index'))


class MailingToggleActiveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "mailing.disable_mailing"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        data = json.loads(request.body)
        mailing.is_active = data["is_active"]
        mailing.save()
        return JsonResponse({"success": True})
