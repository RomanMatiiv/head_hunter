from django.views.generic import TemplateView


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
