import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from accounts.forms import MyCompanyForm
from config.error_handlers import HttpResponseConflict
from junior_hunter.forms import ApplicationForm
from junior_hunter.forms import VacancyForm
from junior_hunter.models import Application
from junior_hunter.models import Company
from junior_hunter.models import Specialty
from junior_hunter.models import Vacancy


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
@method_decorator(login_required, name='post')
class VacancyView(DetailView):
    """ Одна вакансия"""
    template_name = 'junior_hunter/vacancy.html'
    model = Vacancy
    slug_field = 'id'
    slug_url_kwarg = 'vacancy_id'

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)

        if not form.is_valid():
            # TODO вот тут очень странно работает в первый раз при ошибке значение не возвращяет,
            #  тк в методе get форма то не передается
            context = {'form': form,
                       'object': self.get_object()}
            return render(request, self.template_name, context)

        data = form.cleaned_data

        written_username = data['written_username']
        written_phone = data['written_phone']
        written_cover_letter = data['written_cover_letter']
        vacancy = self.get_object()
        user = request.user

        application = Application(
            written_username=written_username,
            written_phone=written_phone,
            written_cover_letter=written_cover_letter,
            vacancy=vacancy,
            user=user,
        )

        try:
            application.save()
        except IntegrityError:
            return HttpResponseConflict(f'Пользователь {user.username}, id={user.id} уже откликался на данную вакансию')

        return redirect('sent')


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


# TODO вынести нечто общее в MyCompanyBase, как минимум LoginRequiredMixin
# TODO поробовать упростить  https://www.agiliq.com/blog/2019/01/django-createview/
# TODO в зависимости от того есть компания или нет отображать или нет боковое меню
class MyCompanyView(LoginRequiredMixin, View):
    def get(self, request):
        # TODO частичное дублирование код, возможно лучше создать get_object_or_none в менеджере объектов
        try:
            company = Company.objects.get(owner_id=request.user.id)
        except ObjectDoesNotExist:
            return redirect('mycompany_letsstart')

        my_company = MyCompanyForm(instance=company)

        context = {'form': my_company}
        return render(request, 'junior_hunter/my-company-edit.html', context)

    def post(self, request):
        # TODO частичное дублирование код, возможно лучше создать get_object_or_none в менеджере объектов
        try:
            company = Company.objects.get(owner_id=request.user.id)
        except ObjectDoesNotExist:
            company = None

        form = MyCompanyForm(instance=company, data=request.POST, files=request.FILES)
        form.instance.owner = request.user
        if form.is_valid():
            form.save()
        return redirect('mycompany')


class MyCompanyCreateView(MyCompanyView):
    def get(self, request):
        context = {'form': MyCompanyForm}
        return render(request, 'junior_hunter/my-company-create.html', context)


class MyCompanyVacancies(LoginRequiredMixin, ListView):
    template_name = 'junior_hunter/my-company-vacancy-list.html'
    model = Vacancy

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.id
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        company = get_object_or_404(Company, owner=self.user_id)
        filtered_queryset = queryset.filter(company_id=company.id)
        return filtered_queryset


class MyCompanyEditVacancy(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        vacancy_id = kwargs['vacancy_id']
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        vacancy_application = vacancy.applications

        vacancy_form = VacancyForm(instance=vacancy)

        context = {'form': vacancy_form,
                   'applications': vacancy_application,
                   }
        return render(request, 'junior_hunter/my-company-vacancy-edit.html', context)

    def post(self, request, *args, **kwargs):
        # TODO дублирование тоже что и в get
        vacancy_id = kwargs['vacancy_id']
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)

        form = VacancyForm(instance=vacancy, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return redirect('mycompany_vacancy_edit', vacancy_id=vacancy_id)


class MyCompanyCreateVacancy(LoginRequiredMixin, View):
    # TODO дублирование MyCompanyEditVacancy
    def get(self, request, *args, **kwargs):
        vacancy_form = VacancyForm()

        context = {'form': vacancy_form}
        return render(request, 'junior_hunter/my-company-vacancy-edit.html', context)

    def post(self, request, *args, **kwargs):
        form = VacancyForm(data=request.POST, files=request.FILES)
        form.instance.company = get_object_or_404(Company, owner=request.user.id)
        form.instance.published_at = datetime.datetime.now()
        if form.is_valid():
            created_vacancy = form.save()
            return redirect('mycompany_vacancy_edit', vacancy_id=created_vacancy.id)
        else:
            context = {'form': form}
            return render(request, 'junior_hunter/my-company-vacancy-edit.html', context)


class MyCompanyLetsStart(LoginRequiredMixin, TemplateView):
    template_name = 'junior_hunter/my-company-letsstart.html'


class SendView(LoginRequiredMixin, TemplateView):
    template_name = 'junior_hunter/sent.html'
