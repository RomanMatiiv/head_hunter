from django.db import models
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import IntegerField
from django.db.models import FloatField
from django.db.models import DateTimeField
from django.db.models import ManyToManyField
from django.db.models import ForeignKey
from django.db.models import URLField


class Company(models.Model):
    name = CharField(max_length=255)
    location = CharField(max_length=255)  # TODO сделать полем с выбором, возможно из другой модели
    logo = URLField(default='https://place-hold.it/100x60')
    description = TextField()
    employee_count = IntegerField()


class Specialty(models.Model):
    code = CharField(max_length=100)  # TODO сделать полем с выбором, возможно из другой модели
    title = CharField(max_length=100)
    picture = URLField(default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = CharField(max_length=100)
    specialty = ForeignKey(Specialty, related_name="vacancies", on_delete=models.PROTECT)
    company = ManyToManyField(Company, related_name="vacancies")
    skills = CharField(max_length=100)  # TODO попробовать ArrayField
    description = TextField()
    salary_min = FloatField()
    salary_max = FloatField()
    published_at = DateTimeField()
