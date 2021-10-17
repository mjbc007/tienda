# Generated by Django 3.2.8 on 2021-10-17 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0004_compra_detallecompra_detallepedido_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallecompra',
            name='compra',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='pedido.compra'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='pedido',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='pedido.pedido'),
            preserve_default=False,
        ),
    ]