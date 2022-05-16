# Generated by Django 4.0.3 on 2022-05-16 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(default=0.0, max_length=8),
        ),
    ]
