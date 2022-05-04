# Generated by Django 4.0.3 on 2022-05-04 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deliver', '0002_alter_car_staff_id_alter_carfordeliver_car_id_and_more'),
        ('product', '0001_initial'),
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='deliver_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_of_this_deliver', to='deliver.deliver'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_num',
            field=models.FloatField(verbose_name='采购数量'),
        ),
        migrations.AlterField(
            model_name='purchasedetail',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='purchase_of_this_product', to='product.product'),
        ),
        migrations.AlterField(
            model_name='purchasedetail',
            name='supplier_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='purchase_of_this_supplier', to='purchase.supplier'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='supplier_charge_phone',
            field=models.PositiveBigIntegerField(verbose_name='供应商负责人电话'),
        ),
        migrations.AlterField(
            model_name='supplierdetail',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='supplier_of_this_product', to='product.product'),
        ),
        migrations.AlterField(
            model_name='supplierdetail',
            name='supplier_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_of_this_supplier', to='purchase.supplier'),
        ),
    ]
