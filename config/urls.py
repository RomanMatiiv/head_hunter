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

from accounts.views import MyLoginView
from accounts.views import MyLogoutView
from accounts.views import RegisterView
from config.error_handlers import custom_handler400
from config.error_handlers import custom_handler403
from config.error_handlers import custom_handler404
from config.error_handlers import custom_handler500
from junior_hunter.views import AllVacanciesView
from junior_hunter.views import CategoryVacancyView
from junior_hunter.views import CompanyView
from junior_hunter.views import MainPageView
from junior_hunter.views import MyCompanyCreateVacancy
from junior_hunter.views import MyCompanyCreateView
from junior_hunter.views import MyCompanyEditVacancy
from junior_hunter.views import MyCompanyLetsStart
from junior_hunter.views import MyCompanyVacancies
from junior_hunter.views import MyCompanyView
from junior_hunter.views import SendView
from junior_hunter.views import VacancyView

# TODO структурировать url
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', MainPageView.as_view(), name='main'),

    path('login', MyLoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', MyLogoutView.as_view(), name='logout'),

    path('vacancies/', AllVacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:category>', CategoryVacancyView.as_view(), name='category_vacancies'),
    path('companies/<int:company_id>', CompanyView.as_view(), name='company'),

    path('sent', SendView.as_view(), name='sent'),

    path('mycompany', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/create', MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/letsstart', MyCompanyLetsStart.as_view(), name='mycompany_letsstart'),
    path('mycompany/vacancies/', MyCompanyVacancies.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/edit/<int:vacancy_id>', MyCompanyEditVacancy.as_view(), name='mycompany_vacancy_edit'),
    path('mycompany/vacancies/create/', MyCompanyCreateVacancy.as_view(), name='mycompany_vacancy_create'),


]

# TODO разобрать что это и как работает
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler400 = custom_handler400
handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500
