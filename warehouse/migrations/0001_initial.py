# Generated by Django 4.0.3 on 2022-05-03 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('warehouse_flow', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('left_num', models.FloatField(max_length=8)),
                ('warehouse_status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Inward',
            fields=[
                ('purchase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='purchase.purchase')),
                ('in_time', models.DateTimeField()),
                ('warehouse_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouse')),
            ],
        ),
    ]
