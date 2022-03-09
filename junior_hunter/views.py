from django.db.models import Count
from django.views.generic import TemplateView

from junior_hunter.models import Specialty, Company


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


# – Все вакансии списком  /vacancies
class AllVacanciesView(TemplateView):
    # TODO переделать шаблон тк этот похож на вакансии по категориям
    template_name = 'junior_hunter/vacancies.html'


# – Карточка компании  /companies/345
class CompanyView(TemplateView):
    template_name = 'junior_hunter/company.html'
