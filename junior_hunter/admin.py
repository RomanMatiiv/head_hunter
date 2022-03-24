from django.contrib import admin

from junior_hunter.models import Application
from junior_hunter.models import Company
from junior_hunter.models import Vacancy


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass
