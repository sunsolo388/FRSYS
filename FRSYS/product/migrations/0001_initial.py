
# Generated by Django 3.2.9 on 2022-05-19 20:36

# Generated by Django 4.0.4 on 2022-05-14 19:20


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=20)),
                ('product_type', models.CharField(max_length=20)),
                ('product_price', models.FloatField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseDemand',
            fields=[
                ('pdemand_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('pdemand_num', models.FloatField(max_length=8)),
                ('pdemand_time', models.DateField()),
                ('pdemand_state', models.BooleanField(default=0)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
