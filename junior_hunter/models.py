from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import TextField
from django.db.models import URLField


class Company(models.Model):
    def __str__(self):
        return self.name

    name = CharField(max_length=255)
    location = CharField(max_length=255)  # TODO сделать полем с выбором, возможно из другой модели
    logo = URLField(default='https://place-hold.it/100x60')
    description = TextField()
    employee_count = IntegerField()


class Specialty(models.Model):
    def __str__(self):
        return self.title

    code = CharField(max_length=100, primary_key=True)  # TODO сделать полем с выбором, возможно из другой модели
    title = CharField(max_length=100)
    picture = URLField(default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    def __str__(self):
        return self.title

    title = CharField(max_length=100)
    specialty = ForeignKey(Specialty, related_name="vacancies", on_delete=models.PROTECT)
    company = ForeignKey(Company, related_name="vacancies", on_delete=models.PROTECT)
    skills = CharField(max_length=100)
    description = TextField()
    salary_min = IntegerField()
    salary_max = IntegerField()
    published_at = DateTimeField()
