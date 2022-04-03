from pyexpat import model

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from junior_hunter.models import Specialty, Application
from junior_hunter.models import Company
from junior_hunter.models import Vacancy
from junior_hunter.forms import ApplicationForm
from django.contrib.auth.models import User


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

    # TODO разобраться почему не работает аутентификация, точнее когда не залогинен
    # @login_required(login_url=reverse_lazy('login'))
    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            written_username = data['written_username']
            written_phone = data['written_phone']
            written_cover_letter = data['written_cover_letter']
            vacancy = self.get_object()
            # user = request.user
            user = User.objects.get(id=1)

            application = Application(
                written_username=written_username,
                written_phone=written_phone,
                written_cover_letter=written_cover_letter,
                vacancy=vacancy,
                user=user,
            )
            application.save()

        return HttpResponseRedirect(reverse_lazy('success_application'))


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


# TODO переделать на DetailView
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

