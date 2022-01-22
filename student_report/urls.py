
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import assignment_file, atc_wise_export_csv, certificate, course_completed,deactivate_study_center, enrollments, export_csv_exam_assignment, export_csv, export_csv_individual_assignments, export_csv_individual_exams, fee_paid_students, grade_assignment, individual_student_report, reactivate_study_center, registered_study_centers, study_center_enrollments, view_student_reports

app_name='student_report'
urlpatterns = [
    path('report/',view_student_reports,name='view_student_reports'),
    path('report/generate-csv/',export_csv,name='export_csv'),
    path('report/<str:username>/',individual_student_report,name='individual_student_report'),
    path('report/<str:username>/assignment',export_csv_individual_assignments, name='individual_student_report_assignments'),
    path('report/<str:username>/exam',export_csv_individual_exams, name='individual_student_report_exams'),
    path('report/<str:username>/<str:assignment>/grade/',assignment_file, name='assignment_file'),
    path('report/<str:username>/<str:assignment>/enter-grade/',grade_assignment, name="grade_assignment"),
    path('report/<str:username>/exam-and-assignment/',export_csv_exam_assignment, name='individual_student_report_exams_assignments'),
    path('report/enrollments/<str:course>/',enrollments,name="enrollments"),
    path('fee-payment-status/',fee_paid_students,name="fee_paid_students"),
    path('study-center-report/study-centers/',registered_study_centers,name="study_center"),
    path('deactivate/<str:code>/',deactivate_study_center,name="deactivate_study_center"),
    path('reactivate/<str:code>/', reactivate_study_center,name="reactivate_study_center"),
    path('study-center-report/study-centers/<int:study_center_id>/',study_center_enrollments, name="study_center_enrollments"),
    path('study-center-report/study-centers/<int:study_center_id>/export/', atc_wise_export_csv, name="study_center_enrollments_export"),
    path('issue-certificate/', course_completed,name="issue_certificate"),
    path('certificate/<str:course>/<str:username>/', certificate, name="certified"),
]

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
