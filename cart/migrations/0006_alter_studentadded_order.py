# Generated by Django 3.2.4 on 2021-08-09 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_order_order_id'),
        ('cart', '0005_studentadded_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentadded',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.order'),
        ),
    ]
