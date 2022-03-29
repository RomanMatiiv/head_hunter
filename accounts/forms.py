from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'password',
                  )

        labels = {'username': 'Логин'}


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True})
    )