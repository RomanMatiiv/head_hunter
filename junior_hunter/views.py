from django.db.models import Count
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from junior_hunter.models import Specialty, Company, Vacancy


# – Главная  /
class MainPageView(TemplateView):
    template_name = 'junior_hunter/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(count_vacancy=Count('vacancies__id'))
        context['companies'] = Company.objects.annotate(count_vacancy=Count('vacancies__id'))
        return context


# – Одна вакансия /vacancies/22
class VacancyView(TemplateView):
    template_name = 'junior_hunter/vacancy.html'


# – Вакансии по специализации /vacancies/cat/frontend
class CategoryVacancyView(TemplateView):
    template_name = 'junior_hunter/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        specialty_code = kwargs['category']
        specialty = get_object_or_404(Specialty, code=specialty_code)
        context['specialty'] = specialty

        filtered_vacancies = Vacancy.objects.filter(specialty__code=specialty_code)
        context['vacancies'] = filtered_vacancies
        context['vacancies_count'] = filtered_vacancies.count()

        return context


# – Все вакансии списком  /vacancies
class AllVacanciesView(TemplateView):
    template_name = 'junior_hunter/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vacancies = Vacancy.objects.all()
        context['vacancies'] = vacancies
        context['vacancies_count'] = vacancies.count()

        return context


# – Карточка компании  /companies/345
class CompanyView(TemplateView):
    template_name = 'junior_hunter/company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company_id = kwargs['company_id']
        company = get_object_or_404(Company, id=company_id)
        context['company'] = company

        filtered_vacancies = Vacancy.objects.filter(company__id=company_id)
        context['vacancies'] = filtered_vacancies
        context['vacancies_count'] = filtered_vacancies.count()

        return context


# TODO повторяющиеся части, которые нужно вынести в общий шаблон
    # * все ваканси
    # * вакансии по специализации
    # * вакансии компании
    # везде есть список вакансий различается лишь шапка поэтому нужно в общий шаблон вынести