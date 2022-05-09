# Generated by Django 4.0.4 on 2022-05-09 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=20, verbose_name='密码')),
                ('mail', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('tel', models.PositiveBigIntegerField(verbose_name='电话号码')),
                ('identity', models.PositiveIntegerField(choices=[(0, '客户'), (1, '员工')], default=0, verbose_name='状态')),
            ],
        ),
    ]
