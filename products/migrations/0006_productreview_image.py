# Generated by Django 5.2.1 on 2025-06-18 19:00

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dvyz3blnz/image/upload/v1748718456/samples/shoe.jpg', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]
