from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from user.forms import NewUserForm


class ProfileView(TemplateView):
    template_name = "user/profile.html"


class RegisterFormView(FormView):
    template_name = "user/register.html"
    form_class = NewUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Inscription réussie !" )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de l'inscription.")
        return super().form_invalid(form)
