from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as DjangoLoginView

from .forms import LoginForm, SignupForm


class LoginView(DjangoLoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response

