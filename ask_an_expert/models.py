from django.db import models
from accounts.models import User
from .choices import *
from courses.models import Course
# Create your models here.

class CourseCategories(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    category_slug = models.CharField(max_length=100)
    def __str__(self):
        return f' {self.course} -- Category: {self.category}'

class Question(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    category = models.CharField(choices=CATEGORY_CHOICE,max_length=20,default='word')
    body = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} -- {self.title}'


class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    body = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Response from - {self.user}'
