from django.urls import path

from accounts.views import MyLoginView
from accounts.views import MyLogoutView
from accounts.views import RegisterView

urlpatterns = [
    path('login', MyLoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', MyLogoutView.as_view(), name='logout'),
]