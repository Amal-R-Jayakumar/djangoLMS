
from college_or_atc.models import StudyCenter
from courses.models import Course, Enrollment, ConductTest, SubmitAssignment, AssignmentGrading
from django import forms
from django.http.response import HttpResponse
from accounts.models import User, Profile, Contact
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ContactForm, NonStudentUserUpdateForm, SignupProfileForm, UserLoginForm, UserSignUpForm, userUpdateForm, profileUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail

# Create your views here.

# redirection decorator


def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


@login_excluded('accounts:home')
def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        # next = request.user.get('next')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = Profile.objects.filter(user=user).first()
            qualification = profile.qualification
            address = profile.address
            if user.user_type == 1:
                if user.gender != "" and qualification != "" and address != "":
                    return redirect('courses:courses')
                else:
                    return redirect('accounts:profile')
            else:
                return redirect('student_report:view_student_reports')

    context = {'title': 'IT Kerala | Login', 'form': form, }
    return render(request, 'accounts/login.html', context)


@login_excluded('accounts:home')
def signup(request):
    sign_up_form = UserSignUpForm(None)
    profile_form = SignupProfileForm(None)
    if request.method == 'POST':
        sign_up_form = UserSignUpForm(request.POST)
        profile_form = SignupProfileForm(request.POST)
        if sign_up_form.is_valid() and profile_form.is_valid():
            username = sign_up_form.cleaned_data.get('email')
            contact_number = sign_up_form.cleaned_data.get('contact_number')
            name = sign_up_form.cleaned_data.get('name')
            email = sign_up_form.cleaned_data.get('email')
            gender = sign_up_form.cleaned_data.get('gender')
            dob = profile_form.cleaned_data.get('dob')
            address = profile_form.cleaned_data.get('address')
            qualification = profile_form.cleaned_data.get('qualification')
            password1 = sign_up_form.cleaned_data.get('password1')
            password2 = sign_up_form.cleaned_data.get('password2')

            if password1 != password2:
                sign_up_form.add_error(field='password2',
                                       error='Passwords Do Not Match')
            else:
                try:
                    user = User.objects.create_user(
                        username=username, name=name, contact_number=contact_number, gender=gender, email=email, password=password1)
                    profile = Profile.objects.create(
                        user=user, dob=dob, address=address, qualification=qualification)
                    # return redirect('accounts:home')
                except:
                    user = None
                if user != None:
                    send_mail('Credentials - MORE 2019',
                    f'Greetings,\n\nThese are your login credentials for IT Kerala - MORE 2019. \nLogin Email: {email}, \nPassword: {password1}.\n\nHappy Learning,\n IT Kerala Team',
                    'noreply@itkeralaedu.com',[email],fail_silently=False)
                    login(request, user)
                    profile.save()
                    return redirect('accounts:home')
                else:
                    request.session['register_error'] = 1
    context = {'title': 'Registration',
               'sign_up_form': sign_up_form, 'profile_form': profile_form}
    return render(request, 'accounts/signup.html', context)


def home(request):
    sw_course_count = Course.objects.filter(category=1).count()
    hw_course_count = Course.objects.filter(category=2).count()
    mm_course_count = Course.objects.filter(category=3).count()
    form = ContactForm(None)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        form.save()
    logged_in = request.user.is_authenticated
    user = request.user
    context = {
        'title': 'IT Kerala',
        'logged_in': logged_in,
        'sw_course_count': sw_course_count,
        'hw_course_count': hw_course_count,
        'mm_course_count': mm_course_count,
        'user': user,
        'form': form,

    }
    return render(request, 'index.html', context)


@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        u_form = NonStudentUserUpdateForm(request.POST, instance=user)
        if request.user.user_type == 1:u_form = userUpdateForm(request.POST, instance=user)


        p_form = profileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if p_form.is_valid():  # u_form.is_valid() and
            user_save = u_form.save(commit=False)
            user_save.user = request.user
            user_save.save()
            profile_save = p_form.save(commit=False)
            profile_save.user = request.user
            profile_save.save()
            # profile_submission.save()
            messages.success(
                request, 'Your account has been successfully updated!')
            # return redirect('courses:courses')

            return redirect('accounts:change_password')
    else:
        u_form = NonStudentUserUpdateForm(instance=user)
        if request.user.user_type == 1:
            u_form = userUpdateForm(instance=user)
        p_form = profileUpdateForm(instance=user.profile)

    context = {
        'title': 'IT Kerala | Update Profile',
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        # 'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def view_user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if user.user_type == 1:
        try:
            assignment_mark_list = SubmitAssignment.objects.filter(user=user)
            graded_assignment_mark_list = assignment_mark_list.filter(
                graded=True)
            assignment_mark = sum(
                [i.grade for i in graded_assignment_mark_list])
        except:
            assignment_mark = None
        try:
            total_exam_marks = sum(
                [i.marks for i in ConductTest.objects.filter(user=user)])
        except:
            total_exam_marks = None
    else:
        assignment_mark = None
        total_exam_marks = None
        assignment_mark_list = None
    context = {
        'title': 'IT Kerala | Profile',
        'profile': profile,
        'user': user,
        'assignment_mark': assignment_mark,
        'total_exam_marks': total_exam_marks,

    }
    return render(request, 'accounts/view_user_profile.html', context)

@login_required
def performance_analysis(request):
    enrolls = Enrollment.objects.filter(student=request.user)
    performance_list={}
    for enrollment in enrolls:
        avg_submitted_assignments = AssignmentGrading.objects.filter(
            student=request.user)
        attended_tests = ConductTest.objects.filter(user=request.user)
        performance_list[enrollment.course.course_name] = {"test_assignment": [], 'total_in_assignments':0,'total_in_tests':0}
        for session in enrollment.course.session_set.all():
            if ConductTest.objects.filter(session=session).filter(user=request.user) or AssignmentGrading.objects.filter(session=session).filter(student=request.user):
                performance_list[enrollment.course.course_name]["test_assignment"].append({"session":session,"exam": ConductTest.objects.filter(session=session).filter(user=request.user).first(), "assignment": AssignmentGrading.objects.filter(session=session).filter(student=request.user).first()})
            else:
                break
        performance_list[enrollment.course.course_name]['total_in_assignments'] = sum([each_assignment_submitted.assignment_avg_marks for each_assignment_submitted in avg_submitted_assignments])
        performance_list[enrollment.course.course_name]['total_in_tests'] = sum([each_test_attended.marks for each_test_attended in attended_tests])
        performance_list[enrollment.course.course_name]['grand_total'] = performance_list[enrollment.course.course_name]['total_in_tests'] + performance_list[enrollment.course.course_name]['total_in_assignments']
    context = {
        'title': 'IT Kerala | Performance',
        'avg_submitted_assignments': avg_submitted_assignments,
        'attended_tests': attended_tests,
        'performance_list': performance_list,
        }

    return render(request, 'accounts/performance.html', context)


def error_404(request, *exception,**kwargs):
    data = {'title':'404'}
    return render(request, '404.html', data)


def error_500(request,  *exception):
    data = {}
    return render(request, '500.html', data)


def error_403(request, *exception):
    data = {}
    return render(request, '403.html', data)


def csrf_failure(request, reason=""):
    data = {}
    return render(request, '403.html', data)


@login_required
def enquiry(request):
    context = {
        'title': 'IT Kerala | Enquiry',
        'contacts': Contact.objects.all()
    }
    return render(request, 'accounts/enquiry.html', context)


@login_required
def send_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # send_mail('Credentials - MORE 2019',
        #           f'Greetings,\n\nThese are your login credentials for IT Kerala - MORE 2019. \nLogin Email: {email}, \nPassword: 45@GLRpuaos.\n\nHappy Learning,\n IT Kerala Team',
        #           'noreply@itkeralaedu.com', [email], fail_silently=False)
        send_mail('IT Kerala Edu',
                  f"Greetings,\n\nThere was a slight technical issue from our part. That's why you were not able to login. We've since fixed the issue. Please login again and attend your course.",'noreply@itkeralaedu.com', [email], fail_silently=False)
        return HttpResponse('Email response '+email)
    return render(request, 'email.html',)


# @login_required
# def study_center(request,code):
#     study_center = StudyCenter.objects.filter(admin_user=request.user)
#     study_center_code = StudyCenter
