from courses.models import Course
from accounts.models import User
from django.db import models

# Create your models here.


class Certificate(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    certifide = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name + " - " +self.course.course_name


class StudentFeedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField()

    def __str__(self):
        return self.student.name + " - " + self.course.course_name
