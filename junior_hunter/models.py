from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # TODO сделать полем с выбором, возможно из другой модели
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()


class Specialty(models.Model):
    code = models.CharField(max_length=100)  # TODO сделать полем с выбором, возможно из другой модели
    title = models.CharField(max_length=100)
    picture = models.URLField(default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.PROTECT)
    company = models.ManyToManyField(Company, related_name="vacancies")
    skills = models.CharField(max_length=100)  # TODO попробовать ArrayField
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateTimeField()
