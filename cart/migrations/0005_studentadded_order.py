# Generated by Django 3.2.4 on 2021-08-09 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_order_order_id'),
        ('cart', '0004_delete_feepaidstudents'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentadded',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='payments.order'),
            preserve_default=False,
        ),
    ]
