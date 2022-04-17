import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

# from accounts.forms import MyAuthenticationForm
from accounts.forms import RegisterForm

logger = logging.getLogger(__name__)


# TODO переделать на RedirectView или LogoutView
class LogoutView(View):
    template_name = 'accounts/login.html'  # TODO посмотреть действительно ли я использую в этой вьюхе шаблон

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main')


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
