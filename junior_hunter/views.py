from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render


# – Главная  /
class MainPageView(TemplateView):
    template_name = 'index.html'


# – Одна вакансия /vacancies/22
class VacancyView(TemplateView):
    template_name = 'vacancy.html'


# – Вакансии по специализации /vacancies/cat/frontend
class CategoryVacancyView(TemplateView):
    template_name = 'vacancies.html'


# – Все вакансии списком  /vacancies
class AllVacanciesView(TemplateView):
    # TODO переделать шаблон тк этот похож на вакансии по категориям
    template_name = 'vacancies.html'


# – Карточка компании  /companies/345
class CompanyView(TemplateView):
    template_name = 'company.html'
