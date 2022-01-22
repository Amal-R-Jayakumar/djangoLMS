from django.db.models import fields
from rest_framework import serializers
from courses.models import Course, Enrollment
from accounts.models import User,Profile
from college_or_atc.models import StudyCenter

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'college','assignments_total_obtainable_marks','total_obtainable_marks']


class StudyCenterSerializer(serializers.ModelSerializer):
    college = EnrollmentSerializer(read_only=True)
    class Meta:
        model = StudyCenter
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    course = EnrollmentSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ["id", "course_name", "slug", "course"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    student = EnrollmentSerializer(read_only=True)
    admin_user = StudyCenterSerializer(read_only=True)
    user = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['name','username','email','contact_number','password','user','admin_user','student']
