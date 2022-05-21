
# Generated by Django 3.2.9 on 2022-05-19 20:36

# Generated by Django 4.0.4 on 2022-05-14 19:20


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inward',
            fields=[
                ('purchase_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='purchase.purchase')),
                ('warehouse_flow', models.CharField(default=0, max_length=8, unique=True)),
                ('in_time', models.DateTimeField()),
                ('in_num', models.FloatField(default=0, max_length=8)),
                ('product_name', models.CharField(default='苹果', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Outward',
            fields=[
                ('outward_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('out_num', models.FloatField(max_length=8)),
                ('out_time', models.DateTimeField()),
                ('product_name', models.CharField(max_length=20)),
                ('warehouse_flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.inward', to_field='warehouse_flow')),
            ],
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_num', models.FloatField(max_length=8)),
                ('warehouse_status', models.CharField(default='库存', max_length=10)),
                ('product_name', models.CharField(default='苹果', max_length=20)),
                ('warehouse_flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.inward', to_field='warehouse_flow')),
            ],
            options={
                'unique_together': {('warehouse_flow', 'warehouse_status')},
            },
        ),
    ]
