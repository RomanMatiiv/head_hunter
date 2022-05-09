from django.urls import path

from junior_hunter.views import MyCompanyCreateVacancy
from junior_hunter.views import MyCompanyCreateView
from junior_hunter.views import MyCompanyEditVacancy
from junior_hunter.views import MyCompanyLetsStart
from junior_hunter.views import MyCompanyVacancies
from junior_hunter.views import MyCompanyView

urlpatterns = [
    path('', MyCompanyView.as_view(), name='mycompany'),
    path('create', MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('letsstart', MyCompanyLetsStart.as_view(), name='mycompany_letsstart'),
    path('vacancies/', MyCompanyVacancies.as_view(), name='mycompany_vacancies'),
    path('vacancies/edit/<int:vacancy_id>', MyCompanyEditVacancy.as_view(), name='mycompany_vacancy_edit'),
    path('vacancies/create/', MyCompanyCreateVacancy.as_view(), name='mycompany_vacancy_create'),
]