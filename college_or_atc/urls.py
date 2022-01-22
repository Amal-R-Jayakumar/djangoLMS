from college_or_atc.views import add_atc, add_students, college_added_student, create_study_center, college_added_student_verification, edit_atc_from_admin, verify_student_added_by_college
from django.urls import path

app_name='study_center'

urlpatterns=[
    path('study-center/',create_study_center,name='create_study_center'),
    path('study-center/add-student/',add_students,name="add_students"),
    path('add-study-center/', add_atc, name="add_atc"),
    path('add-students/<str:code>/', add_students, name="add_students_admin"),
    path('study-center/edit/<int:id>/', edit_atc_from_admin, name="edit_atc_details"),
    path('college/add-students/',college_added_student,name="add_student_college"),
    path('college/add-students/<str:code>/',college_added_student_verification,name="approve_students_college"),
    path('college/add-students/<int:id>/verify/',verify_student_added_by_college, name="verify_students_college"),
]
