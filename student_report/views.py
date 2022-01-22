from student_report.models import Certificate
from cart.models import StudentAdded
from college_or_atc.models import StudyCenter
from django.shortcuts import render
from courses.forms import GradeAssignmentForm
from django.utils import timezone
from django.http import response
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from courses.models import Course, Enrollment, ConductTest, SubmitAssignment, Session, Assignment, AssignmentGrading
import csv
import datetime
from itertools import chain
from django.shortcuts import HttpResponse
from mimetypes import guess_type
from wsgiref.util import FileWrapper
from django.core.mail import BadHeaderError, send_mail
from student_report.filters import StudyCenterFiltering
# Create your views here.


@login_required
def view_student_reports(request):
    students = User.objects.filter(user_type=1)
    if request.user.user_type == 3:
        institute = get_object_or_404(StudyCenter, admin_user=request.user)
        enrollments = Enrollment.objects.filter(
            course__slug="more-2019").filter(student__user_type=1).filter(college=institute).order_by('-enrollment_date')
    else:
        enrollments = Enrollment.objects.filter(
            course__slug="more-2019").filter(student__user_type=1).order_by('-enrollment_date')
    total_assignment_count = SubmitAssignment.objects.all().count()
    total_exam_count = Session.objects.all().count()
    today = timezone.now().date()
    assignment_cumulative = AssignmentGrading.objects.all()
    context = {
        'title': 'IT Kerala | Student Report ',
    }
    msg = None
    if request.user in students:
        msg = 'No Access for Students'
        context['msg'] = msg
    else:
        context['today'] = today
        context['students'] = students
        context['enrollments'] = enrollments
        context['total_assignment_count'] = total_assignment_count
        context['total_exam_count'] = total_exam_count

    return render(request, 'student_report/get_report.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=student_data{datetime.datetime.now()}.csv'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Course', 'Exams Attended', 'Cumilative total in exams', 'Assignments Submitted',
                    'Assignments Graded Till Now', 'Marks Obtained', 'Total accumulated till now'])
    courses = Course.objects.all()
    if request.user.user_type == 4 or request.user.user_type == 5 or request.user.user_type == 2:
        students = User.objects.filter(user_type=1)
        print(students.count())
        for course in courses:
            for student in students:
                if Enrollment.objects.filter(student=student).filter(course=course):
                    try:
                        assignment_mark = Enrollment.objects.filter(student=student).filter(
                            course__slug=course.slug).first().assignment_marks
                    except:
                        assignment_mark = 0
                    try:
                        exam_marks = student.enrollment_set.filter(
                            course__slug=course.slug).first().final_cumulative_marks
                    except AttributeError:
                        exam_marks = 0
                    writer.writerow([student.name, course, student.conducttest_set.all().count(), exam_marks, student.submitassignment_set.all().count(),
                                     student.submitassignment_set.filter(graded=True).count(), assignment_mark, assignment_mark+exam_marks])
    elif request.user.user_type == 3:
        enrollment_list = Enrollment.objects.filter(college=StudyCenter.objects.get(
            admin_user=request.user)).filter(student__user_type=1)
        for student in enrollment_list:
            try:
                assignment_mark = student.assignment_marks
            except:
                assignment_mark = 0
            try:
                exam_marks = student.final_cumulative_marks
            except:
                exam_marks = 0
            writer.writerow([student.student.name, student.course.course_name, student.student.conducttest_set.all().count(), exam_marks, student.student.submitassignment_set.all().count(),
                             student.student.submitassignment_set.filter(graded=True).count(), assignment_mark, assignment_mark+exam_marks])
    return response


@login_required
def individual_student_report(request, username):
    student = get_object_or_404(User, username=username)
    max_assignment_marks = Assignment.objects.all().count()*4
    assignment_obtained_marks = get_object_or_404(
        Enrollment, student=student).assignment_marks
    exam_total = get_object_or_404(
        Enrollment, student=student).final_cumulative_marks
    final_total = assignment_obtained_marks+exam_total
    course = get_object_or_404(Enrollment, student=student).course.slug
    context = {
        'title': 'IT Kerala | Individual Student Report',
    }

    if request.user.user_type == 1:
        return Http404
    else:
        context['student'] = student
        context['course'] = course
        context['enrollment'] = student.enrollment_set.all().first()

        context['exams'] = student.conducttest_set.all()
        context['submitted_assignments'] = student.submitassignment_set.all()
        context['assignment_obtained_marks'] = assignment_obtained_marks
        context['assignment_percentage'] = round((
            assignment_obtained_marks/244)*100, 2)
        context['exam_percentage'] = round((
            student.enrollment_set.all().first().final_cumulative_marks/272)*100, 2)
        context['max_assignment_marks'] = max_assignment_marks
        context['final_total'] = final_total
        context['final_total_percentage'] = round((final_total/516)*100,2)

    return render(request, 'student_report/student_data.html', context)


@login_required
def export_csv_individual_assignments(request, username):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={username}_assignments.csv'
    writer = csv.writer(response)
    writer.writerow(['Assignment', 'Submission date'])

    student = User.objects.get(username=username)
    for assignment in student.submitassignment_set.all():
        writer.writerow(
            [assignment.assignment, assignment.submitted_date.date()])

    return response


@login_required
def export_csv_individual_exams(request, username):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={username}_exams.csv'
    writer = csv.writer(response)
    writer.writerow(['Exams Attended', 'Marks Obtained'])

    student = User.objects.get(username=username)

    for exam in student.conducttest_set.all():
        writer.writerow([exam.session.session, exam.marks])
    return response


@login_required
def export_csv_exam_assignment(request, username):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={username}student_data_exams{datetime.datetime.now()}.csv'
    writer = csv.writer(response)
    student = User.objects.get(username=username)
    writer.writerow(['Student:', student.name])
    writer.writerow([' ', ' '])
    writer.writerow([' ', ' '])
    exams = student.conducttest_set.all()
    assignments = student.submitassignment_set.all()

    sessions_attended = [exam.session.session for exam in exams]
    marks_obtained = [exam.marks for exam in exams]
    assignments_completed = [
        assignment.assignment.assignment_name for assignment in assignments]
    assignments_day = [
        assignment.lesson.session.session for assignment in assignments]
    assignments_completed_date = [
        assignment.submitted_date.date() for assignment in assignments]
    assignments_graded = [
        'Yes' if assignment.graded else 'No' for assignment in assignments]
    assignments_grade_obtained = [
        assignment.grade for assignment in assignments]

    data = {
        'Exams Attended': sessions_attended, 'Marks Obtained': marks_obtained, 'Assignment Day': assignments_day,

        'Assignment': assignments_completed, 'Submission date': assignments_completed_date, 'Graded': assignments_graded, 'Grade obtained': assignments_grade_obtained,
    }
    max_n = max([len(x) for x in data.values()])
    for field in data:
        data[field] += [''] * (max_n - len(data[field]))

    writer.writerow(data.keys())
    writer.writerows(zip(*data.values()))

    return response


def assignment_file(request, assignment, username):
    assignment_file = SubmitAssignment.objects.filter(
        user__username=username).filter(assignment__id=assignment).first().assignment_file

    # print(f'\n\n{assignment_file.split()}\n\n')

    # with open(assignment_file, 'rb') as f:
    #     wrapper = FileWrapper(f)
    mimetype = "application/force-download"
    guessed_type = guess_type(str(assignment_file))[0]
    if guessed_type:
        mimetype = guessed_type
    response = HttpResponse(assignment_file, mimetype)
    response['Content-Disposition'] = f"attachment;filename={assignment_file}"
    return response


@login_required
def grade_assignment(request, username, assignment):
    submission = SubmitAssignment.objects.filter(
        user__username=username).filter(assignment__id=assignment).first()
    form = GradeAssignmentForm()
    student = get_object_or_404(User, username=username)
    assignment = get_object_or_404(Assignment, id=assignment)
    error = None
    lesson = submission.lesson
    session = lesson.session
    lesson_qs = session.lesson_set.all()

    assignment_count = 0
    for each_lesson in lesson_qs:
        assignment_count += each_lesson.assignment_set.count()

    if request.method == "POST":
        form = GradeAssignmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('grade')
            if data <= 4:
                submission.grade_assignment(data)
                submitted_assignments_in_sessions = list(chain(
                    *[list(SubmitAssignment.objects.filter(user=student).filter(lesson=lesson)) for lesson in lesson_qs]))

                avg_assignment_marks = sum(
                    [i.grade for i in submitted_assignments_in_sessions])/assignment_count

                if not AssignmentGrading.objects.filter(student=student).filter(session=session):
                    AssignmentGrading.objects.create(
                        student=student, session=session, assignment_avg_marks=avg_assignment_marks)
                else:
                    submission_graded = False
                    for assignment in submitted_assignments_in_sessions:
                        if not assignment.graded:
                            submission_graded = False
                            break
                        else:
                            submission_graded = True
                    AssignmentGrading.objects.filter(student=student).filter(session=session).update(
                        assignment_avg_marks=avg_assignment_marks, all_graded=submission_graded)
                    assignment_total = sum(
                        [i.assignment_avg_marks for i in AssignmentGrading.objects.filter(student=student)])
                    print(f'\n\n{assignment_total}\n\n')
                    assignment_marks_enrollment = Enrollment.objects.filter(
                        student=student).filter(course=session.course).first()
                    assignment_marks_enrollment.assignment_marks = assignment_total
                    assignment_marks_enrollment.save()
                return redirect('student_report:individual_student_report', username=username)
            else:
                error = 'Maximum marks per assignment is 4'

    context = {'form': form, 'submissions': submission,
               'error': error, 'student': student, 'assignment': assignment, }
    return render(request, 'student_report/grade_form.html', context)


@login_required
def enrollments(request, course):
    if request.user.user_type == 5:
        enrollments = Enrollment.objects.filter(
            course__slug=course).exclude(student__user_type=5)
        context = {
            'enrollments': enrollments
        }
        return render(request, 'student_report/enrollment.html', context)
    else:
        return Http404


@login_required
def fee_paid_students(request):
    students = StudentAdded.objects.all()
    context = {'title': 'IT Kerala | Student Fee Payment Status',
               'students': students}
    return render(request, 'student_report/fee_status.html', context)


@login_required
def registered_study_centers(request):
    study_centers = StudyCenter.objects.all()
    district_filter = StudyCenterFiltering(request.GET, queryset=study_centers)
    study_centers = district_filter.qs
    return render(request, 'student_report/study_centers.html', context={'title': 'IT Kerala | Study Centers', 'study_centers': study_centers, 'district_filter': district_filter, })


@login_required
def deactivate_study_center(request, code):
    user = StudyCenter.objects.get(code=code).admin_user
    user.is_active = False
    user.save()
    # send_mail('Account Deactivation',
    # f'Greetings,\n\nWe detected a malpractice from your account. Contact Kerala State RUTRONIX or Principle Affiliate to activate your account. \n\nIT Kerala Team',
    # 'noreply@itkeralaedu.com',[email],fail_silently=False)
    return redirect('student_report:study_center')


@login_required
def reactivate_study_center(request, code):
    user = StudyCenter.objects.get(code=code).admin_user
    user.is_active = True
    user.save()
    # send_mail('Account Deactivation',
    # f'Greetings,\n\nWe have reactivated your account. \n\nIT Kerala Team',
    # 'noreply@itkeralaedu.com',[email],fail_silently=False)
    return redirect('student_report:study_center')


@login_required
def study_center_enrollments(request, study_center_id):
    study_center = get_object_or_404(StudyCenter, id=study_center_id)
    enrollments = Enrollment.objects.filter(
        college__id=study_center_id).filter(student__user_type=1)
    today = timezone.now().date()
    enrollments_from_today = Enrollment.objects.filter(enrollment_date=today).filter(
        college__id=study_center_id).filter(student__user_type=1).count()
    context = {
        'title': f'IT Kerala | {study_center.name}',
        'enrollments': enrollments,
        'study_center': study_center,
        'today': today,
        'enrollments_from_today': enrollments_from_today,
    }
    return render(request, 'student_report/atc_wise_report.html', context)


@login_required
def atc_wise_export_csv(request, study_center_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=student_data{datetime.datetime.now()}.csv'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Exams Attended', 'Cumilative total in exams', 'Assignments Submitted',
                    'Assignments Graded Till Now', 'Marks Obtained', 'Total accumulated till now'])
    courses = Course.objects.all()
    if request.user.user_type == 4 or request.user.user_type == 5 or request.user.user_type == 2:
        students = User.objects.filter(user_type=1)

        for course in courses:
            for student in students:
                if Enrollment.objects.filter(student=student).filter(course=course).filter(college=StudyCenter.objects.get(id=study_center_id)):
                    try:
                        assignment_mark = Enrollment.objects.filter(student=student).filter(college__id=study_center_id).filter(
                            course__slug=course.slug).first().assignment_marks
                    except:
                        assignment_mark = 0
                    try:
                        exam_marks = student.enrollment_set.filter(
                            course__slug=course.slug).first().final_cumulative_marks
                    except AttributeError:
                        exam_marks = 0
                    writer.writerow([student.name, course.course_name, student.conducttest_set.all().count(), exam_marks, student.submitassignment_set.all().count(),
                                    student.submitassignment_set.filter(graded=True).count(), assignment_mark, assignment_mark+exam_marks])
    elif request.user.user_type == 3 or request.user.user_type == 1:
        return Http404
    return response


@login_required
def course_completed(request):
    student_list = []
    courses = Course.objects.all()

    for course in courses:
        enrollments = Enrollment.objects.filter(
            course=course).filter(student__user_type=1)
        for each_enrollment in enrollments:
            session = each_enrollment.course.session_set.last()
            print(session)
            session_test = ConductTest.objects.filter(
                user=each_enrollment.student).filter(session=session)
            assignment_graded = AssignmentGrading.objects.filter(
                student=each_enrollment.student).filter(session=session)

            if Certificate.objects.filter(student=each_enrollment.student).filter(course=course):
                certificate_status = True
            else:
                certificate_status = False
            if session_test and assignment_graded:
                if each_enrollment.assignment_marks >= each_enrollment.assignments_total_obtainable_marks/2 and each_enrollment.final_cumulative_marks >= each_enrollment.assignments_total_obtainable_marks/2:
                    status = True
                else:
                    status = False
                student_list.append({'each_enrollment': each_enrollment,
                                    'status': status, 'certificate_status': certificate_status})
    for i in student_list:
        print(i)
    context = {'title': 'IT Kerala | Certification',
               'student_lists': student_list}
    return render(request, 'student_report/certification.html', context)


@login_required
def certificate(request, course, username):
    enrollment = get_object_or_404(Enrollment, student__username=username)
    course = get_object_or_404(Course, slug=course)
    student = get_object_or_404(User, username=username)
    if request.method == 'GET':
        if not Certificate.objects.filter(student__username=username).filter(course__slug=course.slug):
            Certificate.objects.create(
                student=student, course=course, certifide=True)
    return redirect('student_report:issue_certificate')
