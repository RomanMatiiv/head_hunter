from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField()
    location = models.CharField()  # TODO сделать полем с выбором, возможно из другой модели
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()


class Specialty(models.Model):
    code = models.CharField()  # TODO сделать полем с выбором, возможно из другой модели
    title = models.CharField()
    picture = models.URLField(default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = models.CharField()
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.PROTECT)
    company = models.ManyToManyField(Company, related_name="vacancies")
    skills = models.CharField()  # TODO попробовать ArrayField
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateTimeField()
