# Generated by Django 4.0.4 on 2022-05-08 12:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('deliver', '0005_deliver_aim_add_deliver_start_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliver',
            name='apply_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='申请时间'),
            preserve_default=False,
        ),
    ]