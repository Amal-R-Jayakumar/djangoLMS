# Generated by Django 3.2.4 on 2021-10-18 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20211018_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='correct_ans',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='opt1',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='opt2',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='opt3',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='opt4',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='question',
            field=models.CharField(max_length=1000),
        ),
    ]
