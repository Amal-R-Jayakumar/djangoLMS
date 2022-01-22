from django.urls import path, re_path
from .views import answer_keys, CreateAssignment,enrollment_api, CreateCourse, SubmitAssignmentDetail,rules, UnenrollCourse, enroll_course, enrolled_courses, study_lesson, take_test_view, view_assignment, view_course_details, view_courses, view_marks
from django.conf import settings
from django.conf.urls.static import static



app_name = 'courses'
urlpatterns = [
    path('new-course/', CreateCourse.as_view(), name='new_course'),
    path('courses/', view_courses, name="courses"),
    path('courses/<str:slug>/', view_course_details, name="course_detail"),
    path('courses/<str:course_slug>/<str:lesson_slug>/',study_lesson, name="study_lesson"),
    path('courses/<str:course_slug>/<str:lesson_slug>/assignments/<int:id>/',view_assignment, name='assignment_detail'),  # Also handles assignment submission
    path('courses/<str:course_slug>/<str:lesson_slug>/take-test/',take_test_view, name='take_test'),
    path('courses/<str:course_slug>/<str:session_slug>/marks/',view_marks,name='view_marks'),
    path('enroll/<str:slug>/', enroll_course, name='enroll_course'),
    path('profile/courses/enrolled/',enrolled_courses,name="enrolled_courses"),
    path('unenroll/<str:slug>/', UnenrollCourse.as_view(), name='unenroll_course'),
    path('rules/',rules,name='rules'),
    path('enrollment-api/', enrollment_api, name='enrollment-api'),
    path('answer-keys/', answer_keys,name="answer-key"),

]
# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
