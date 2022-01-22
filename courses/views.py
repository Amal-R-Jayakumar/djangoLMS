from django.http.response import JsonResponse, Http404
from cart.models import StudentCart
from college_or_atc.forms import StudyCenterForm
from college_or_atc.models import StudyCenter
import os
import datetime
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from .models import ConductTest, Course, Enrollment, Assignment, TestQuestion, Lesson, Resource, Assignment, Session, SubmitAssignment,AnswerKey
from .forms import EnrollmentForm, GradeAssignmentForm, CreateAssignmentForm, SubmitAssignmentForm
from accounts.models import Profile, User
from itertools import chain
from django.db import IntegrityError
from courses.serializers import UserSerializer,ProfileSerializer,StudyCenterSerializer,EnrollmentSerializer,CourseSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import BadHeaderError, send_mail
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def rules(request):
    context = {
        'title': 'I T Kerala | Rules'
    }
    return render(request, 'rules.html', context)


class CreateCourse(LoginRequiredMixin, generic.CreateView):
    fields = ('course_name', 'course_description')
    model = Course

    def get(self, request, *args, **kwargs):
        self.object = None
        context_dict = self.get_context_data()
        context_dict.update(user_type=self.request.user.user_type)
        return self.render_to_response(context_dict)

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super(CreateCourse, self).form_valid(form)


class CourseDetail(DetailView):
    template_name = 'course'
    model = Course
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        assignments = Assignment.objects.filter(course=self.kwargs['pk'])
        resources = Resource.objects.filter(course=self.kwargs['pk'])
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['assignments'] = assignments
        context['resources'] = resources
        return context


@login_required
def view_courses(request):  # ListCourse Class
    courses = Course.objects.all()
    enrollment = Enrollment.objects.filter(student=request.user)
    is_enrolled = False
    if enrollment:
        is_enrolled = True
    # Should move course ENROLLMENT to VIEW_COURSE_DETAILS function when multiple courses are added as the above method has a bug.
    context = {
        'title': 'IT Kerala | Courses',
        'courses': courses,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/courses.html', context)


@login_required
def view_course_details(request, slug):
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        raise Http404
    is_enrolled = course.enrollment_set.filter(student__username=request.user.username).first()
    sessions = course.session_set.all()

    week_dates = []
    if is_enrolled:
        day = timezone.now().date() - is_enrolled.enrollment_date
        week_dates = [is_enrolled.enrollment_date +
                      datetime.timedelta(days=i) for i in range(day.days+1)]

        # holidays = [datetime.date(2021, 8, 20), datetime.date(2021, 8, 21), datetime.date(2021, 8, 23), datetime.date(2021, 12, 25)]

        for date in week_dates:
            if date.weekday() == 6:
                week_dates.remove(date)
        if course.slug == 'more-2019' and Enrollment.objects.filter(course__slug='more-2019').filter(college__institute=1):
            for date in week_dates:
                if date.weekday() == 5:
                    week_dates.remove(date)

        # for date in week_dates:
        #     if date in holidays:
        #         week_dates.remove(date)

        if not is_enrolled.enrollment_date in week_dates:
            week_dates.insert(0, is_enrolled.enrollment_date)
    error = None
    if not week_dates:
        error = 'You are not enrolled in this course yet.'
    open_days = len(week_dates)
    # last_active_sessions = course.session_set.order_by('id').filter(session_number=len(week_dates)).first()
    context = {
        'title': f'IT Kerala | {course.course_name}',
        'course': course,
        'sessions': sessions,
        'is_enrolled': is_enrolled,
        # 'last_active_sessions': last_active_sessions,
        'day': open_days,
        'error': error,
    }
    return render(request, 'courses/course_details.html', context)


@login_required
def study_lesson(request, **kwargs):
    course = Course.objects.get(slug=kwargs.pop('course_slug'))
    lesson = Lesson.objects.get(slug=kwargs.pop('lesson_slug'))

    is_enrolled = course.enrollment_set.filter(student__username=request.user.username).first()

    sessions = course.session_set.order_by('session_number')[:0]
    is_expired = False
    current_session = lesson.session
    previous_session = Session.objects.filter(pk__lt=current_session.pk).order_by('-pk').first()
    week_dates = []

    assignments_completed = None

    if is_enrolled:
        open_days = None
        day = timezone.now().date() - is_enrolled.enrollment_date
        week_dates = [is_enrolled.enrollment_date +
                      datetime.timedelta(days=i) for i in range(day.days+1)]

        # This statement is placed here so that the course completion can be given 9in absolute value.
        if len(week_dates) > course.completion_time.days*2:
            is_expired = True

        # holidays = [datetime.date(2021, 8, 15), datetime.date(2021, 8, 20), datetime.date(2021, 8, 21), datetime.date(2021, 8, 23), datetime.date(2021, 12, 25)]

        for date in week_dates:
            if date.weekday() == 6:
                week_dates.remove(date)
        if course.slug == 'more-2019' and Enrollment.objects.filter(course__slug='more-2019').filter(college__institute=1):
            for date in week_dates:
                if date.weekday() == 5:
                    week_dates.remove(date)

        # for date in week_dates:
        #     if date in holidays:
        #         week_dates.remove(date)

        if not is_enrolled.enrollment_date in week_dates:
            week_dates.insert(0, is_enrolled.enrollment_date)

        open_days = len(week_dates)

        sessions = course.session_set.order_by('id')[:open_days]

    resource = Resource.objects.filter(lesson=lesson).first()
    pdf_resource_file = None
    if resource:
        pdf_resource_file = resource.resource_link

    try:
        is_improved = current_session.conducttest_set.filter(user=request.user).first().is_improved
    except AttributeError:
        is_improved = None

    tests = None
    assignments_completed = None
    if previous_session:
        tests = previous_session.conducttest_set.filter(user__username=request.user.username).filter(session=previous_session).first()
        lesson_qs = previous_session.lesson_set.all()
        assignments_completed = (
            len(list(chain(*[list(SubmitAssignment.objects.filter(user=request.user).filter(lesson=lesson)) for lesson in lesson_qs]))) >= len(list(chain(*[list(Assignment.objects.filter(lesson=lesson)) for lesson in lesson_qs]))))

    assignments = lesson.assignment_set.all()
    context = {
        'title': f'IT Kerala | {lesson}',
        'course': course,
        'lesson': lesson,
        'sessions': sessions,
        'current_session': current_session,
        'assignments': assignments,
        'assignments_completed': assignments_completed,
        'is_enrolled_student': is_enrolled,
        'is_expired': is_expired,
        'previous': previous_session,
        'tests': tests,
        'open_days': open_days,
        'is_improved': is_improved,
        'resource_files': pdf_resource_file,
        # "images": img_list,
    }
    return render(request, 'courses/study_lesson.html', context)


@login_required
def enroll_course(request, **kwargs):
    course = get_object_or_404(Course, slug=kwargs.get('slug'))
    # Since Each Session Contains a quiz with 4 questions
    total_obtainable_marks = course.session_set.all().count()*4
    category = course.category.category_name
    if category == 'Software':
        institutes = StudyCenter.objects.filter(software=True).filter(institute=1)
    elif category == 'Hardware':
        institutes = StudyCenter.objects.filter(hardware=True).filter(institute=1)
    elif category == 'Multimedia':
        institutes = StudyCenter.objects.filter(
            multimedia=True).filter(institute=1)
    error= None
    if request.method == 'POST':
        if request.POST['institute'] != "Select Training Center":
            college = StudyCenter.objects.get(id=request.POST['institute'])
            if course.price == 0:
                try:
                    Enrollment.objects.create(student=request.user, course=course, college=college, total_obtainable_marks=total_obtainable_marks)
                except IntegrityError:
                    messages.warning(request, 'You are already enrolled in the course.')
                    return redirect('courses:course_detail', slug=kwargs.get('slug'))
            else:
                try:
                    StudentCart.objects.create(course=course,user=request.user,price=course.price,college=college)
                except IntegrityError:
                    pass
            return redirect('payment_gateway:payment')
            # else:
            #     messages.success(request, 'You are now enrolled in the course.')
            #     return redirect('courses:course_detail', slug=kwargs.get('slug'))
        else:
            error = 'Select an Option'
    context = {'title': 'IT Kerala | Enroll',
               'institutes': institutes, 'course': course, 'error':error}
    return render(request,'courses/enroll-course.html', context)


class UnenrollCourse(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('courses:courses')

    def get(self, *args, **kwargs):
        try:
            enrollment = Enrollment.objects.filter(
                student=self.request.user, course__pk=self.kwargs.get('slug')).get()
        except Enrollment.DoesNotExist:
            messages.warning(
                self.request, 'You are not enrolled in this course.')
        else:
            enrollment.delete()
            messages.success(
                self.request, 'You have unenrolled from the course.')
        return super().get(self.request, *args, **kwargs)


@login_required
def enrolled_courses(request):
    enrolled_course_list = Enrollment.objects.filter(student=request.user)
    context = {
        'title': 'IT Kerala | Enrolled Courses',
        'enrolled_course_list': enrolled_course_list,
    }
    return render(request, 'accounts/enrolled-courses.html', context)

####################################################################
####################################################################
############################ RESOURCES ###########################
####################################################################
####################################################################

@login_required
def answer_keys(request):
    if not request.user.user_type == 1:
        answer_keys_files = AnswerKey.objects.all()
        context = {
            'title':'IT Kerala | Answer Key',
            'answer_key_files':answer_keys_files,
        }
        return render(request,'courses/answer_key.html', context)
    else:
        raise Http404

@login_required
def delete_resource_view(request, pk):
    obj = get_object_or_404(Resource, pk=pk)
    context = {'resource': obj}
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect(reverse("courses:list"))
    return render(request, "resources/resource_confirm_delete.html", context)


class CreateAssignment(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'courses/create_assignment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UpdateAssignment(LoginRequiredMixin, generic.UpdateView):
    model = Assignment
    form_class = CreateAssignmentForm
    template_name = 'courses/create_assignment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeleteAssignment(LoginRequiredMixin, generic.DeleteView):
    model = Assignment
    success_url = reverse_lazy('courses:list')

####################################################################
####################################################################
############################ ASSIGNMENTS ###########################
####################################################################
####################################################################


@login_required
# Handles Assignment Submissiobn along with viewing
def view_assignment(request, **kwargs):
    assignment = Assignment.objects.get(pk=kwargs.pop('id'))
    course = Course.objects.get(slug=kwargs.pop('course_slug'))
    lesson = Lesson.objects.get(slug=kwargs.pop('lesson_slug'))
    session = lesson.session
    submission_form = SubmitAssignmentForm()
    submission_allowed = False
    if request.user.user_type == 1 or request.user.user_type == 5:
        submission_allowed = True
    elif request.user.user_type == 2:
        submission_allowed = False
    already_submitted = SubmitAssignment.objects.filter(
        user=request.user).filter(assignment=assignment)

    error = None
    if not already_submitted:
        if request.method == 'POST':
            submission_form = SubmitAssignmentForm(request.POST, request.FILES)
            if submission_form.is_valid():
                user = request.user
                submitted_date = timezone.now()
                assignment_file = request.FILES['assignment_file']
                submission_does_exist = SubmitAssignment.objects.filter(
                    user=request.user).filter(assignment=assignment)

                if not submission_does_exist:
                    submission = SubmitAssignment(
                        user=user, lesson=lesson, assignment=assignment, assignment_file=assignment_file, submitted_date=submitted_date)
                    submission.save()
                return redirect('courses:study_lesson', course_slug=course.slug, lesson_slug=lesson.slug)
            else:
                error = 'Please upload in microsoft file format or as a PDF'

    context = {
        'title': 'IT Kerala | Assignments',
        'assignment': assignment,
        'lesson': lesson,
        'session': session,
        'error': error,
        'course': course,
        'submission_form': submission_form,
        'submission_allowed': submission_allowed,
        'already_submitted': already_submitted,
    }
    return render(request, 'courses/assignments.html', context)


class SubmitAssignmentDetail(LoginRequiredMixin, generic.DetailView):
    model = SubmitAssignment
    template_name = 'assignments/submitassignment_detail.html'

    def get_context_data(self, **kwargs):
        submissions = SubmitAssignment.objects.filter(pk=self.kwargs['pk'])
        submissions_object = get_object_or_404(submissions)
        context = super(SubmitAssignmentDetail,
                        self).get_context_data(**kwargs)
        context['submissions'] = submissions_object
        return context


@login_required
def delete_assignments_view(request, pk):
    obj = get_object_or_404(SubmitAssignment, pk=pk)
    context = {'submission': obj}
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect(reverse("courses:list"))
    return render(request, "assignments/submission_confirm_delete.html", context)


@login_required
def take_test_view(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    session = lesson.session
    test_questions = TestQuestion.objects.filter(
        session__slug=session.slug).order_by('?')[:4]

    if request.method == 'POST':
        result = dict(request.POST)
        del result['csrfmiddlewaretoken']
        marks = 0
        for key in result:
            marks += str(TestQuestion.objects.get(id=key).correct_ans).strip() == "".join(result[key]).strip()

        if not ConductTest.objects.filter(user=request.user).filter(session=session):
            if marks < 4:
                object = ConductTest.objects.create(user=request.user, session=session, marks=marks)
            elif marks == 4:
                object = ConductTest.objects.create(user=request.user, session=session, marks=marks, is_improved=True)
            object.save()

        else:
            object = ConductTest.objects.filter(user=request.user).filter(session=session).first()

            if object.marks < 2:
                if marks > object.marks:
                    object = ConductTest.objects.filter(user=request.user).filter(session=session)
                    object.update(marks=marks)
            else:

                if object.marks >= 2 and not object.is_improved:
                    if marks >= 2 and marks > object.marks:
                        object = ConductTest.objects.filter(user=request.user).filter(session=session).update(marks=marks)
                    object = ConductTest.objects.filter(user=request.user).filter(session=session).update(is_improved=True)

                elif object.marks >= 2 and object.is_improved:
                    return redirect('courses:view_marks', course_slug=course_slug, session_slug=session.slug)

        return redirect('courses:view_marks', course_slug=course_slug, session_slug=session.slug)
    context = {'title': 'IT Kerala | Test', 'question_list': test_questions,
               'course_slug': course_slug, 'lesson_slug': lesson_slug}
    return render(request, 'courses/exam.html', context)


@login_required
def view_marks(request, course_slug, session_slug):

    exam = ConductTest.objects.filter(user=request.user)
    last_attended = exam.filter(session__slug=session_slug).first()

    error = 'You can improve the marks obtained once'
    if last_attended.is_improved:
        error = 'You have improved your marks by attending the exam again. The mark obtained now cannot be changed.'

    course = Course.objects.get(slug=course_slug)
    session = Session.objects.get(slug=session_slug)
    lesson = session.lesson_set.all().first()
    cumulative = sum([each_test.marks for each_test in exam])
    enrollment = Enrollment.objects.filter(student=request.user).filter(course=course).first()

    enrollment.final_cumulative_marks = cumulative
    enrollment.save()
    total = enrollment.total_obtainable_marks

    if request.method == "POST":
        last_attended.is_improved = True
        last_attended.save()
        return redirect('courses:course_detail', course_slug)

    context = {
        'title': f'Marks Obtained | {request.user.name}',
        'cumulative': cumulative,
        'exams': exam,
        'last_attended': last_attended,
        'total': total,
        'is_improved': last_attended.is_improved,
        'course': course,
        'lesson': lesson,
        'error': error,
    }
    return render(request, 'courses/view_marks.html', context)


@api_view(['GET','POST'])
def enrollment_api(request):
    if request.method=="GET":
        enrollments = Course.objects.all()
        # users = User.objects.all()
        serialied_data = CourseSerializer(enrollments,many=True)
        # serialied_data = UserSerializer(users,many=True)
        return JsonResponse(serialied_data.data,safe=False)
    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        data = request.data
        email = data.get('email')
        username = data.get('email')
        name = data.get('name')
        contact_number = data.get('contact_number')
        password = User.objects.make_random_password(
            length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889!@#$%^&*()")
        user_data = {"username": username, "email": email, "name": name, "contact_number": contact_number, "password": password}

        if not User.objects.filter(username=username):
            user = UserSerializer(data=user_data)
            if user.is_valid():
                User.objects.create_user(username=username, email=email, name=name, contact_number=contact_number,password=password)
                send_mail('Credentials - MORE 2019',f'Greetings {name},\n\nThese are your login credentials for IT Kerala. \nLogin Email: {email}, \nPassword: {password}.\n\nHappy Learning,\n IT Kerala Team','noreply@itkeralaedu.com',[email],fail_silently=False)
            else:
                return Response(user.errors)
        profile_data={'user':User.objects.get(email=email).id}
        if not Profile.objects.filter(user__username=username):
            profile = ProfileSerializer(data=profile_data)
            if profile.is_valid():
                profile.save()
            else:
                return Response(profile.errors)
        if data.get('course') == "ms-office":
            course = Course.objects.get(slug='more-2019') # COURSE IS HARD CODED. HAD TO BE CHANGED FROM THE OTHER END TOO
        course = Course.objects.get(slug='more-2019')
        marks = course.session_set.count()*4
        try:
            college = StudyCenter.objects.get(code=data.get('code')).id
        except:
            return Response({"code":"Invalid ATC or College Code"})
        enrollment_data = {"student": User.objects.get(email=email).id,"college":college,"course":course.id,"assignments_total_obtainable_marks":marks,'total_obtainable_marks':marks}
        enrollment = EnrollmentSerializer(data=enrollment_data)
        if enrollment.is_valid():
            enrollment.save()
            return JsonResponse(enrollment.data, status=201)
        else:
            return JsonResponse(enrollment.errors, status=400)
