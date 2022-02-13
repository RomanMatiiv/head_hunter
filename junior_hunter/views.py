from django.http import HttpResponse
from django.views import View


# – Главная  /
class MainPageView(View):
    def get(self, request):
        return HttpResponse('Здесь будет главная страница')


# – Одна вакансия /vacancies/22
class VacancyView(View):
    def get(self, request, vacancy_id):
        return HttpResponse("Здесь будет карточка вакансии")


# – Вакансии по специализации /vacancies/cat/frontend
class CategoryVacancyView(View):
    def get(self, request, category):
        return HttpResponse("Здесь будет карточка категории вакансий")


# – Все вакансии списком  /vacancies
class AllVacanciesView(View):
    def get(self, request):
        return HttpResponse("Здесь будет страница со всеми вакансиями")


# – Карточка компании  /companies/345
class CompanyView(View):
    def get(self, request, company_id):
        return HttpResponse("Здесь будет карточка компании")
