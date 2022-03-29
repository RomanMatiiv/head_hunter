import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from accounts.forms import MyAuthenticationForm
from accounts.forms import RegisterForm

logger = logging.getLogger(__name__)


# TODO переделать на RedirectView или LogoutView
class LogoutView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('main'))


# TODO попробовать переписать на CBV
class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html', context={'form': RegisterForm})

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            data = register_form.cleaned_data

            user = User(username=data.get('username'),
                        first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        )
            user.set_password(data.get('password'))
            user.save()

            # TODO сделать редирект на ту же страницу но с зеленой надписью успеха
            # https://getbootstrap.com/docs/4.0/components/alerts/
            return redirect(reverse_lazy('main'))
        else:
            logger.error("invalid form")
            return render(request, 'accounts/register.html', context={'form': register_form})


# TODO попробовать переписать на CBV
class MyLoginView(View):

    def get(self, request):
        form = MyAuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = MyAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('main'))
            else:
                logger.warning('User not found')
        else:
            return render(request, 'accounts/login.html', {'form': form})
