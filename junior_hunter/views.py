from django.db.models import Count
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from junior_hunter.models import Specialty
from junior_hunter.models import Company
from junior_hunter.models import Vacancy


class MainPageView(TemplateView):
    """ Главная  / """
    template_name = 'junior_hunter/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(count_vacancy=Count('vacancies__id'))
        context['companies'] = Company.objects.annotate(count_vacancy=Count('vacancies__id'))
        return context


class VacancyView(DetailView):
    """ Одна вакансия"""
    template_name = 'junior_hunter/vacancy.html'
    model = Vacancy
    slug_field = 'id'
    slug_url_kwarg = 'vacancy_id'


class AllVacanciesView(ListView):
    template_name = 'junior_hunter/vacancies.html'
    model = Vacancy


class CategoryVacancyView(ListView):
    """ Вакансии по специализации """
    template_name = 'junior_hunter/vacancies.html'
    model = Vacancy

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.specialty = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        specialty_code = kwargs['category']
        self.specialty = get_object_or_404(Specialty, code=specialty_code)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty'] = self.specialty
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(specialty__code=self.specialty.code)
        return filtered_queryset


class CompanyView(ListView):
    """Карточка компании"""
    template_name = 'junior_hunter/company.html'
    model = Vacancy

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        company_id = kwargs['company_id']
        self.company = get_object_or_404(Company, id=company_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(company__id=self.company.id)
        return filtered_queryset
