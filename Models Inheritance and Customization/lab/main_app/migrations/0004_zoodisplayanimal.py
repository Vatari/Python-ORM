# Generated by Django 5.0.4 on 2024-07-07 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_rename_licens_number_veterinarian_license_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZooDisplayAnimal',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_app.animal',),
        ),
    ]