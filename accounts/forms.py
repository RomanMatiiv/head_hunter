from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from junior_hunter.models import Company


class RegisterForm(UserCreationForm):
    password2 = None

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'password1',
                  )
        labels = {'username': 'Логин'}


# class MyAuthenticationForm(AuthenticationForm):
#     username = UsernameField(
#         label='Логин',
#         widget=forms.TextInput(attrs={'autofocus': True})
#     )

class MyCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['owner']
