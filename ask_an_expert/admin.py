from django.contrib import admin
from .models import Question,Response,CourseCategories
# Register your models here.

admin.site.register(CourseCategories)
admin.site.register(Question)
admin.site.register(Response)
