import random

from django.db import migrations


class Migration(migrations.Migration):

    def generate_barcodes(apps, schema_editor):
        Product = apps.get_model('main_app', 'Product')
        all_products = Product.objects.all()
        barcodes = random.sample(range(100000000, 1000000000), len(all_products))
        for product, barcode in zip(all_products, barcodes):
            product.barcode = barcode
            product.save()

    def reverse_barcodes(apps, schema_editor):
        Product = apps.get_model('main_app', 'Product')
        all_products = Product.objects.all()
        for product in Product.objects.all():
            product.barcode = 0
            product.save()

    dependencies = [
        ('main_app', '0005_remove_product_count_product_barcode'),
    ]

    operations = [
        migrations.RunPython(generate_barcodes, reverse_barcodes)
    ]
