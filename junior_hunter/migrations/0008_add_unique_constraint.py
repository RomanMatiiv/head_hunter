# Generated by Django 4.0.2 on 2022-04-03 19:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('junior_hunter', '0007_add_change_field_relaton'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('vacancy', 'user')},
        ),
    ]