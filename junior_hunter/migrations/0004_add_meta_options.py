# Generated by Django 4.0.2 on 2022-03-24 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('junior_hunter', '0003_add_owner_field_to_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'companies'},
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name_plural': 'vacancies'},
        ),
    ]
