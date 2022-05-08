# Generated by Django 4.0.4 on 2022-05-08 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_alter_inward_in_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inward',
            name='warehouse_flow',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='warehouse_flow',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='warehouse.inward', to_field='warehouse_flow'),
        ),
    ]
