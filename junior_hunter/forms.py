from django.forms import ModelForm

from junior_hunter.models import Application
from junior_hunter.models import Vacancy


class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        fields = (
            'written_username',
            'written_phone',
            'written_cover_letter',
        )


class VacancyForm(ModelForm):

    class Meta:
        model = Vacancy
        fields = (
            'title',
            'specialty',
            'salary_min',
            'salary_max',
            'skills',
            'description',  # TODO вот здесь нужно как-то от html код превратить в текст
        )
