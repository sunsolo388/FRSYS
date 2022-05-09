# Generated by Django 4.0.4 on 2022-05-09 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('deliver', '0001_initial'),
        ('warehouse', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=8)),
                ('customer_tel', models.CharField(max_length=11)),
                ('customer_cre', models.FloatField(max_length=8)),
                ('customer_add', models.TextField()),
                ('customer_gender', models.BooleanField(verbose_name='性别')),
            ],
        ),
        migrations.CreateModel(
            name='enterprise_flow',
            fields=[
                ('flow_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('reason', models.TextField()),
                ('num', models.FloatField(max_length=8)),
                ('sender', models.CharField(max_length=20)),
                ('receiver', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('order_price', models.FloatField(max_length=8)),
                ('order_time', models.DateTimeField()),
                ('out_time', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.customer')),
                ('deliver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliver.deliver')),
                ('warehouse_flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='AfterSales',
            fields=[
                ('aftersales_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('question_type', models.CharField(max_length=15)),
                ('question_status', models.BooleanField()),
                ('question_discription', models.TextField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_num', models.FloatField(max_length=8)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'unique_together': {('order_id', 'product_id')},
            },
        ),
    ]
