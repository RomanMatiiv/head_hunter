# Generated by Django 4.0.2 on 2022-03-12 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('logo', models.URLField(default='https://place-hold.it/100x60')),
                ('description', models.TextField()),
                ('employee_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('picture', models.URLField(default='https://place-hold.it/100x60')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('skills', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('published_at', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                              related_name='vacancies',
                                              to='junior_hunter.company',
                                              )),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                                related_name='vacancies',
                                                to='junior_hunter.specialty',
                                                )),
            ],
        ),
    ]
