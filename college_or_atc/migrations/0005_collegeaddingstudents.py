# Generated by Django 3.2.4 on 2021-08-30 05:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college_or_atc', '0004_alter_studycenter_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeAddingStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Phone number entered incorrectly.', regex='^(\\+91[\\-\\s]?)?[0]?(91)?[6789]\\d{9}$')])),
                ('study_center', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='college_or_atc.studycenter')),
            ],
        ),
    ]
