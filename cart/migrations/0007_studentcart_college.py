# Generated by Django 3.2.4 on 2021-08-10 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college_or_atc', '0001_initial'),
        ('cart', '0006_alter_studentadded_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcart',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='college_or_atc.studycenter'),
        ),
    ]
