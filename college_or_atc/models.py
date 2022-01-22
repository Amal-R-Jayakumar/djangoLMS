from django.db import models
from accounts.models import User
from college_or_atc.choices import *
from django.core.validators import RegexValidator
from django.utils import timezone
# from courses.models import
# Create your models here.

class StudyCenter(models.Model):
    institute = models.IntegerField(choices=INSTITUTES,default=1)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=200)
    district = models.CharField(max_length=50,choices=DISTRICTS)
    admin_user = models.ForeignKey(User,on_delete=models.CASCADE)
    hardware = models.BooleanField(default=False)
    software = models.BooleanField(default=False)
    multimedia = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.code} - {self.name}, {self.address}'


class CollegeAddingStudents(models.Model):
    study_center = models.ForeignKey(StudyCenter,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    # phone_regex = RegexValidator(
    #     regex=r'^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$', message="Phone number entered incorrectly.")
    date_created = models.DateField(default=timezone.now)
    contact_number = models.CharField(
        max_length=17, blank=True)  # validators=[phone_regex],
    selected_course = models.ForeignKey('courses.Course',models.CASCADE)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.study_center.code} -- {self.study_center.name} -- {self.name}'
