from pyexpat import model

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import SingleObjectMixin

from accounts.forms import MyCompanyForm
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


# возможно от detailView нужно отказаться тк форму сложно обрабатывать
# https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/#using-formmixin-with-detailview
# см https://stackoverflow.com/questions/45659986
class VacancyView(DetailView):
    """ Одна вакансия"""
    template_name = 'junior_hunter/vacancy.html'
    model = Vacancy
    slug_field = 'id'
    slug_url_kwarg = 'vacancy_id'

    # @login_required
    # не работает см https://stackoverflow.com/questions/68810221/
    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)

        if not form.is_valid():
            pass
            # TODO бобавть обработку неправильно заполненной формы
            # TODO бобавть обработку если на вакансию уже откликнулись

        data = form.cleaned_data

        written_username = data['written_username']
        written_phone = data['written_phone']
        written_cover_letter = data['written_cover_letter']
        vacancy = self.get_object()
        user = request.user

        # TODO сделать нормально без костылей
        if user.is_anonymous:
            raise PermissionDenied

        application = Application(
            written_username=written_username,
            written_phone=written_phone,
            written_cover_letter=written_cover_letter,
            vacancy=vacancy,
            user=user,
        )
        application.save()

        return HttpResponseRedirect(reverse_lazy('sent'))


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


# class MyCompanyCreateView(FormView):
#     template_name = 'junior_hunter/my-company-create.html'
#     form_class = MyCompanyForm
#     success_url = ''

# TODO добавить проверку аутентицикации
# TODO поробовать упростить  https://www.agiliq.com/blog/2019/01/django-createview/
class MyCompanyCreateView(View):
    def get(self, request, *args, **kwargs):
        my_company = MyCompanyForm()
        my_company.owner = request.user
        context = {'form': my_company}
        return render(request, 'junior_hunter/my-company-create.html', context)

    def post(self, request, *args, **kwargs):
        form = MyCompanyForm(request.POST, request.FILES)
        form.instance.owner = request.user
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse_lazy('main'))
        return render(request, 'junior_hunter/my-company-create.html', {'form': form})