# Generated by Django 3.2.7 on 2022-05-23 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='staff_id',
            field=models.CharField(default=0, max_length=20, verbose_name='员工编号'),
        ),
    ]