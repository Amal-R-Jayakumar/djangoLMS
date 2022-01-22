import os
from typing_extensions import ParamSpec
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models.fields import CharField
# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Student'), (2, 'Instructor'), (3, 'Study Center'), (4, 'Rutronix'), (5, 'Groware')
    )
    name = models.CharField(max_length=255)
    # phone_regex = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$', message="Phone number entered incorrectly.")
    contact_number = models.CharField(max_length=17, blank=True)#validators=[phone_regex]
    gender = CharField(max_length=30)
    user_type = models.PositiveIntegerField(
        choices=USER_TYPE_CHOICES, default=1)

    def __str__(self):
        return f'{self.id}  -  {self.username}'


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user',on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=400)
    qualification = models.CharField(max_length=300)
    dob = models.DateField(null=True)
    profile_pic = models.ImageField(
        default='images/default.png', upload_to='images/profile_pics')

    def __str__(self):
        return f'{self.user.username}\'s Profile'


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_regex = RegexValidator(
        regex=r'^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$', message="Phone number entered incorrectly.")
    contact_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    message = models.TextField(max_length=400)

    def __str__(self):
        return f'Message from {self.name}'
