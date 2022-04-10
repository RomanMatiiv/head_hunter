"""head_hunter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from config.error_handlers import custom_handler400
from config.error_handlers import custom_handler403
from config.error_handlers import custom_handler404
from config.error_handlers import custom_handler500
from junior_hunter.views import AllVacanciesView
from junior_hunter.views import CategoryVacancyView
from junior_hunter.views import CompanyView
from junior_hunter.views import MainPageView
from junior_hunter.views import VacancyView
from accounts.views import MyLoginView
from accounts.views import LogoutView
from accounts.views import RegisterView

# TODO структурировать url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='main'),
    path('vacancies/', AllVacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:category>', CategoryVacancyView.as_view(), name='category_vacancies'),
    path('companies/<int:company_id>', CompanyView.as_view(), name='company'),
    path('sent', TemplateView.as_view(template_name="junior_hunter/sent.html"), name='sent'),
    path('user_profile', TemplateView.as_view(template_name='junior_hunter/user_profile.html'), name='user_profile'),

    # path('vacancies/<int:vacancy_id>/send/', , name=''),
    # path('mycompany/letsstart/',, name=''),
    # path('mycompany/create/',, name=''),
    # path('mycompany/',, name=''),
    # path('mycompany/vacancies/',, name=''),
    # path('mycompany/vacancies/create/',, name=''),
    # path('mycompany/vacancies/<int:vacancy_id>',, name= ),
    path('login', MyLoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),

]

# TODO разобрать что это и как работает
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler400 = custom_handler400
handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500
