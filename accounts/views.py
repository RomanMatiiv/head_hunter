import logging

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from accounts.forms import RegisterForm

logger = logging.getLogger(__name__)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('main')


# TODO попробовать переписать на CBV
class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html', context={'form': RegisterForm})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
        return render(request, 'accounts/register.html', context={'form': register_form})


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('mycompany')
