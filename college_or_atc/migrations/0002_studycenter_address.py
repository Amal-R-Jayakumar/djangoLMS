# Generated by Django 3.2.4 on 2021-08-12 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_or_atc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studycenter',
            name='address',
            field=models.TextField(default='Address', max_length=200),
            preserve_default=False,
        ),
    ]
