# Generated by Django 5.0.4 on 2024-06-24 17:56

from django.db import migrations


def create_unique_brands(apps, schema_editor):
    shoe = apps.get_model('main_app', 'Shoe')
    unique_brands = apps.get_model('main_app', 'UniquesBrands')

    unique_brand_names = shoe.objects.values_list('brand', flat=True).distinct()
    unique_brands.objects.bulk_create([unique_brands(brand_name) for brand_name in unique_brand_names])


def reverse_unique_brands(apps, schema_editor):
    unique_brands = apps.get_model('main_app', 'UniquesBrands')
    unique_brands.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0002_uniquesbrands'),
    ]

    operations = [
        migrations.RunPython(create_unique_brands, reverse_code=reverse_unique_brands)
    ]
