from django.contrib import admin
from .models import *
# Register your models here.


class GroupMemberInline(admin.TabularInline):
    model = Enrollment

admin.site.register(Course)
admin.site.register(Resource)
admin.site.register(Assignment)
admin.site.register(AssignmentGrading)
admin.site.register(Session)
admin.site.register(Lesson)
admin.site.register(SubmitAssignment)
admin.site.register(Enrollment)
admin.site.register(TestQuestion)
admin.site.register(ConductTest)
admin.site.register(Category)
admin.site.register(AnswerKey)
# This exists in Courses Applictions above Enrollment Class.
