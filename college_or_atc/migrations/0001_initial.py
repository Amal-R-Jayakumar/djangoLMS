# Generated by Django 3.2.4 on 2021-08-08 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.IntegerField(choices=[(1, 'ATC'), (2, 'College')], default=1)),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('hardware', models.BooleanField(default=False)),
                ('software', models.BooleanField(default=False)),
                ('multimedia', models.BooleanField(default=False)),
                ('admin_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
