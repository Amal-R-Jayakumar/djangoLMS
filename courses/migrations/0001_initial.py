# Generated by Django 3.2.4 on 2021-08-08 11:39

import courses.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('college_or_atc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=200)),
                ('assignment_description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/assignments')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=200)),
                ('slug', models.SlugField(default='', editable=False, max_length=255)),
                ('course_description', models.TextField()),
                ('course_image', models.ImageField(default='images/default.png', upload_to='images/course_images')),
                ('completion_time', models.DurationField()),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.category')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['course_name'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(default='', editable=False, max_length=255)),
                ('video_url', models.URLField()),
                ('lesson_number', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_number', models.IntegerField()),
                ('session', models.CharField(max_length=100)),
                ('slug', models.SlugField(default='', editable=False, max_length=255)),
                ('is_open', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=400)),
                ('opt1', models.CharField(max_length=100)),
                ('opt2', models.CharField(max_length=100)),
                ('opt3', models.CharField(max_length=100)),
                ('opt4', models.CharField(max_length=100)),
                ('correct_ans', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.session')),
            ],
        ),
        migrations.CreateModel(
            name='SubmitAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_file', models.FileField(upload_to=courses.models.user_directory_path)),
                ('submitted_date', models.DateTimeField()),
                ('graded', models.BooleanField(default=False)),
                ('grade', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='courses.assignment')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(max_length=200)),
                ('resource_link', models.URLField(max_length=300)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.session'),
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateField(default=django.utils.timezone.now)),
                ('assignment_marks', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('assignments_total_obtainable_marks', models.IntegerField(default=0)),
                ('final_cumulative_marks', models.IntegerField(default=0)),
                ('total_obtainable_marks', models.IntegerField(default=0)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college_or_atc.studycenter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('course', 'student')},
            },
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='student_course', through='courses.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ConductTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('marks', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)])),
                ('is_improved', models.BooleanField(default=False)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentGrading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_avg_marks', models.DecimalField(decimal_places=2, max_digits=3)),
                ('all_graded', models.BooleanField(default=False)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson'),
        ),
    ]
