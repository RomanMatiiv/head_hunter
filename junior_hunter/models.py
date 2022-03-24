from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.db.models import ImageField
from django.db.models import OneToOneField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import TextField
from django.db.models import URLField

from config.settings import MEDIA_COMPANY_IMAGE_DIR
from config.settings import MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    """Компания"""
    name = CharField(max_length=255)
    location = CharField(max_length=255)  # TODO сделать полем с выбором, возможно из другой модели
    logo = ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = TextField()
    employee_count = IntegerField()
    owner = OneToOneField(User, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class Specialty(models.Model):
    """Специальность"""
    code = CharField(max_length=100, primary_key=True)  # TODO сделать полем с выбором, возможно из другой модели
    title = CharField(max_length=100)
    picture = ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    """Вакансия"""
    title = CharField(max_length=100)
    specialty = ForeignKey(Specialty, related_name='vacancies', on_delete=models.PROTECT)
    company = ForeignKey(Company, related_name='vacancies', on_delete=models.PROTECT)
    skills = CharField(max_length=100)
    description = TextField()
    salary_min = IntegerField()
    salary_max = IntegerField()
    published_at = DateTimeField()

    class Meta:
        verbose_name_plural = 'vacancies'

    def __str__(self):
        return self.title


class Application(models.Model):
    """Отклик на вакансию"""
    written_username = CharField(max_length=100)
    written_phone = CharField(max_length=31)
    written_cover_letter = TextField()
    vacancy = ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = OneToOneField(User, related_name='applications', on_delete=models.CASCADE)
