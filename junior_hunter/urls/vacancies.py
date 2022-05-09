from django.urls import path

from junior_hunter.views import AllVacanciesView
from junior_hunter.views import CategoryVacancyView
from junior_hunter.views import SendView
from junior_hunter.views import VacancyView

urlpatterns = [
    path('', AllVacanciesView.as_view(), name='all_vacancies'),
    path('<int:vacancy_id>', VacancyView.as_view(), name='vacancy'),
    path('cat/<str:category>', CategoryVacancyView.as_view(), name='category_vacancies'),
    path('sent', SendView.as_view(), name='sent'),
]