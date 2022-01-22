from payments.models import Order
from django.db.models.fields.related import OneToOneField
from courses.models import Course
from college_or_atc.models import StudyCenter
from accounts.models import User
from django.db import models
from django.utils import timezone
# Create your models here.

class StudentAdded(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.ForeignKey(StudyCenter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    fee_paid = models.BooleanField(default=False)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        verbose_name_plural = "Students Added"

    def __str__(self):
        return f'{self.student.name} ADDED FOR {self.course.course_name} AT {self.college.name}'

class StudentCart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    college = models.ForeignKey(StudyCenter,null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.course} ADDED BY {self.user.name}'

    class Meta:
        verbose_name_plural = "Students' Cart"

        
class StudyCenterCart(models.Model):
    study_center_admin_user = OneToOneField(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_students = models.IntegerField(default=0)
    college = models.OneToOneField(StudyCenter, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.study_center_admin_user} Students ADDED BY {self.study_center_admin_user.name}'

    class Meta:
        verbose_name_plural = "ATC or College Cart"
