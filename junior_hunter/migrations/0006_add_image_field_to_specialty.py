# Generated by Django 4.0.2 on 2022-03-24 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('junior_hunter', '0005_add_image_field_to_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(upload_to='speciality_images'),
        ),
    ]
