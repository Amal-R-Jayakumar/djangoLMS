from django.http.response import Http404, JsonResponse
from courses.models import Course, Enrollment
from cart.models import StudentAdded, StudyCenterCart
from django.db import IntegrityError
from accounts.models import Profile, User
from college_or_atc.models import CollegeAddingStudents, StudyCenter
from college_or_atc.forms import ATCProfileForm, AddATCAdminForm, AddStudentForm, CollegeAddingStudentsForm, StudentProfileForm, StudyCenterForm, AddStudentAdminForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, message, send_mail
from django.contrib import messages
# Create your views here.


@login_required
def create_study_center(request):
    context = {'title': 'IT Kerala'}
    if request.user.user_type == 3:
        if not StudyCenter.objects.filter(admin_user=request.user):
            form = StudyCenterForm()
            if request.method == 'POST':
                form = StudyCenterForm(request.POST)
                if form.is_valid():
                    institute = form.cleaned_data.get('institute')
                    name = form.cleaned_data.get('name')
                    code = form.cleaned_data.get('code')
                    address = form.cleaned_data.get('address')
                    district = form.cleaned_data.get('disctict')
                    hardware = form.cleaned_data.get('hardware')
                    software = form.cleaned_data.get('software')
                    multimedia = form.cleaned_data.get('multimedia')
                    if StudyCenter.objects.filter(code=code):
                        form.add_error(
                            field='code', error='Study Center Already Exists')
                    else:
                        StudyCenter.objects.create(institute=institute, name=name, address=address, district=district,
                                                   code=code, hardware=hardware, software=software, multimedia=multimedia, admin_user=request.user)
                        return redirect('accounts:view_profile')
            context = {'title': 'IT Kerala', 'form': form}
        else:

            context = {'title': 'IT Kerala',
                       'study_center': StudyCenter.objects.get(admin_user=request.user)}

    return render(request, 'college_or_atc/register_atc.html', context)


@login_required
def add_students(request):
    student_user_form = AddStudentForm(None)
    profile_form = StudentProfileForm(None)
    study_center = StudyCenter.objects.get(admin_user=request.user)
    courses = Course.objects.all()
    if not study_center.software:
        courses = courses.exclude(category__id=1)
    if not study_center.hardware:
        courses = courses.exclude(category__id=2)
    if not study_center.multimedia:
        courses = courses.exclude(category__id=3)
    students = StudentAdded.objects.filter(college=StudyCenter.objects.get(
        admin_user=request.user)).filter(fee_paid=False)
    context = {'title': 'IT Kerala | Register Student to Course',
               'student_user_form': student_user_form, "profile_form": profile_form, 'courses': courses, 'students': students}
    if request.method == 'POST' and 'AddStudent' in request.POST:
        student_user_form = AddStudentForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        if student_user_form.is_valid() and profile_form.is_valid():
            name = student_user_form.cleaned_data.get('name')
            email = student_user_form.cleaned_data.get('email')
            contact_number = student_user_form.cleaned_data.get(
                'contact_number')
            gender = student_user_form.cleaned_data.get('gender')
            qualification = profile_form.cleaned_data.get('qualification')
            course_id = request.POST.get('course_id')
            if course_id == '' or course_id == 'Select Course':
                context['error'] = 'Select a Course.'
            else:
                user = User.objects.get(email=email)
                course = Course.objects.get(id=course_id)
                if user:
                    if not Enrollment.objects.filter(course=course).filter(student=user):
                        try:
                            StudentAdded.objects.create(
                                student=user, course=course, college=StudyCenter.objects.get(admin_user=request.user))
                        except IntegrityError:
                            context['error'] = 'Student already enrolled for this course.'
                    else:
                        context['error'] = 'Student already enrolled for this course.'
                else:
                    password = User.objects.make_random_password(
                        length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889!@#$%^&*()")
                    user = User.objects.create(
                        username=email, name=name, contact_number=contact_number, email=email, gender=gender)
                    print(f'\n\n{password}\n\n')
                    user.set_password(password)
                    user.save()
                    Profile.objects.create(
                        user=user, qualification=qualification)
                    StudentAdded.objects.create(
                        student=user, course=course, college=StudyCenter.objects.filter(admin_user=request.user))
                    # send_mail('Credentials - MORE 2019',
                    #           f'Greetings,\n\nThese are your login credentials for IT Kerala - MORE 2019. \nLogin Email: {email}, \nPassword: {password}.\n\nHappy Learning,\n IT Kerala Team',
                    #           'noreply@itkeralaedu.com', [email], fail_silently=False)
                    return redirect('study_center:add_students')
        else:
            context['error'] = 'Please fill out the form correctly.'
    elif request.method == 'POST' and 'PayForStudents' in request.POST:
        total_price = sum([each_student.course.price for each_student in StudentAdded.objects.filter(
            college=StudyCenter.objects.get(admin_user=request.user)).filter(fee_paid=False)])
        try:
            StudyCenterCart.objects.create(study_center_admin_user=request.user, price=total_price, number_of_students=StudentAdded.objects.filter(
                college=StudyCenter.objects.get(admin_user=request.user)).count(), college=StudyCenter.objects.get(admin_user=request.user))
        except IntegrityError:
            StudyCenterCart.objects.filter(study_center_admin_user=request.user).update(price=total_price, number_of_students=StudentAdded.objects.filter(
                college=StudyCenter.objects.get(admin_user=request.user)).count(), college=StudyCenter.objects.get(admin_user=request.user))
        return redirect('payment_gateway:payment')
        # pass
    return render(request, 'college_or_atc/add-student.html', context)


@login_required
def add_atc(request):
    if request.user.user_type == 5:
        atc_user_form = AddATCAdminForm(None)
        atc_profile_form = ATCProfileForm(None)
        study_center_form = StudyCenterForm(None)
        if request.method == 'POST':
            atc_user_form = AddATCAdminForm(request.POST)
            atc_profile_form = ATCProfileForm(request.POST)
            study_center_form = StudyCenterForm(request.POST)
            if atc_user_form.is_valid() and atc_profile_form.is_valid() and study_center_form.is_valid():
                name = atc_user_form.cleaned_data.get('name')
                email = atc_user_form.cleaned_data.get('email')
                contact_number = atc_user_form.cleaned_data.get(
                    'contact_number')
                address = atc_profile_form.cleaned_data.get('address')
                district = study_center_form.cleaned_data.get('district')
                institute = study_center_form.cleaned_data.get('institute')
                institute_name = study_center_form.cleaned_data.get('name')
                institute_address = study_center_form.cleaned_data.get(
                    'address')
                code = study_center_form.cleaned_data.get('code')
                a, b, c = True if request.POST.get('software') else False, True if request.POST.get(
                    'hardware') else False, True if request.POST.get('multimedia') else False
                password = User.objects.make_random_password(
                    length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889!@#$%^&*()")
                if not User.objects.filter(email=email):
                    if district == "Select District":
                        study_center_form.add_error(
                            field='district', error="Choose District")
                    else:
                        user = User.objects.create(
                            username=email, name=name, contact_number=contact_number, email=email, user_type=3)
                        user.set_password(password)
                        user.save()
                        Profile.objects.create(user=user, address=address)
                        StudyCenter.objects.create(institute=institute, name=institute_name, address=institute_address,
                                                   district=district, code=code, admin_user=user, software=a, hardware=b, multimedia=c)

                        send_mail('Credentials - IT Kerala',
                                  f'Greetings,\n\nWelcome to IT Kerala. These are your login credentials.\nsite: itkeralaedu.com \nLogin Email: {email}, \nPassword: {password}.\n\n\n IT Kerala Team',
                                  'noreply@itkeralaedu.com', [email], fail_silently=False)
                        return redirect('study_center:add_atc')
                else:
                    atc_user_form.add_error(
                        error="User already exists", field="email")
                # send_mail('Credentials - IT Kerala',
                #           f'Greetings,\n\nThese are your login credentials for IT Kerala. \nLogin Email: {email}, \nPassword: {password}.\n\n\n IT Kerala Team',
                #           'noreply@itkeralaedu.com', [email], fail_silently=False)
                return redirect('study_center:add_atc')

        context = {
            'title': "IT Kerala | Register ATC",
            'atc_user_form': atc_user_form,
            'atc_profile_form': atc_profile_form,
            'study_center_form': study_center_form,
        }
        return render(request, 'college_or_atc/add_atc_from_admin.html', context)
    else:
        raise Http404


@login_required
def edit_atc_from_admin(request,id):
    if request.user.user_type == 5:
        instance = StudyCenter.objects.get(id=id)
        study_center_form = StudyCenterForm(None,instance=instance)
        context = {
            'title': "IT Kerala | Edit ATC",
        }
        context['study_center_form'] = study_center_form
        if request.method == 'POST':
            study_center_form = StudyCenterForm(request.POST,instance=instance)
            if study_center_form.is_valid():
                district = study_center_form.cleaned_data.get('district')
                institute = study_center_form.cleaned_data.get('institute')
                institute_name = study_center_form.cleaned_data.get('name')
                institute_address = study_center_form.cleaned_data.get(
                    'address')
                code = study_center_form.cleaned_data.get('code')
                a, b, c = True if request.POST.get('software') else False, True if request.POST.get(
                    'hardware') else False, True if request.POST.get('multimedia') else False
                password = User.objects.make_random_password(
                    length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889!@#$%^&*()")

                if district == "Select District":
                    study_center_form.add_error(
                        field='district', error="Choose District")
                else:
                    StudyCenter.objects.filter(id=id).update(institute=institute, name=institute_name, address=institute_address,
                                                district=district, code=code, software=a, hardware=b, multimedia=c)
                    messages.success(request,'ATC Details Successfully updated')
                return redirect('student_report:study_center_enrollments',id)

        return render(request, 'college_or_atc/add_atc_from_admin.html', context)
    else:
        raise Http404


@login_required
def add_students(request, code):
    if request.user.user_type == 5:
        student_form = AddStudentAdminForm(None)
        atc = StudyCenter.objects.get(code=code)

        if atc.software:
            courses = Course.objects.filter(category=1)
        elif atc.hardware:
            courses = Course.objects.filter(category=2)
        elif atc.multimedia:
            courses = Course.objects.filter(category=3)
        if request.method == 'POST':
            student_form = AddStudentAdminForm(request.POST)
            if student_form.is_valid():
                email = student_form.cleaned_data.get('email')
                course_slug = request.POST['course']
                try:
                    course = Course.objects.get(slug=course_slug)
                except Course.DoesNotExist:
                    messages.warning(request, 'Invalid Course Selection.')
                    return redirect('study_center:add_students_admin', code=code)
                marks = course.session_set.all().count()*4
                name = student_form.cleaned_data.get('name')
                contact_number = student_form.cleaned_data.get(
                    'contact_number')
                if User.objects.filter(email=email):
                    user = User.objects.get(email=email)
                    if not Enrollment.objects.filter(course__slug=course_slug).filter(student__email=email):
                        Enrollment.objects.create(student=user, college=atc, course=course,assignments_total_obtainable_marks=marks, total_obtainable_marks=marks)
                    else:
                        messages.warning(
                            request, 'This student is already enrolled in this course.')
                else:
                    password = User.objects.make_random_password(
                        length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889!@#$%^&*()")
                    user = User.objects.create(
                        username=email, email=email, name=name, contact_number=contact_number)
                    print(password)
                    user.set_password(password)
                    user.save()
                    Profile.objects.create(user=user)
                    Enrollment.objects.create(student=user, college=atc, course=course,
                                              assignments_total_obtainable_marks=marks, total_obtainable_marks=marks)
                    send_mail('Credentials - MORE 2019',
                              f'Greetings {name},\n\nYou have been add to the {course} at {atc.name}, {atc.address} These are your login credentials for IT Kerala. \nLogin Email: {email}, \nPassword: {password}.\n\nHappy Learning,\n IT Kerala Team', 'noreply@itkeralaedu.com', [email], fail_silently=False)
                return redirect('study_center:add_students_admin', code=code)
        context = {
            'title': 'IT Kerala | Add Students',
            'student_form': student_form,
            'courses': courses,
        }
        return render(request, 'college_or_atc/add_student_from_admin.html', context)
    else:
        raise Http404


@login_required
def college_added_student(request):
    # study_center = StudyCenter.objects.filter(admin_user=request.user).filter(institute=2).first()
    try:
        study_center = StudyCenter.objects.filter(
            admin_user=request.user).filter(institute=2).first()
    except:
        raise Http404
    context = {
        'title': 'IT Kerala | Add Students'
    }
    if request.user.user_type == 3 and study_center.institute == 2:
        form = CollegeAddingStudentsForm(None)
        if request.method == 'POST':
            form = CollegeAddingStudentsForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                if not CollegeAddingStudents.objects.filter(email=email):
                    name = form.cleaned_data.get('name')
                    contact_number = form.cleaned_data.get('contact_number')
                    selected_course = form.cleaned_data.get('selected_course')
                    study_center = StudyCenter.objects.get(
                        admin_user=request.user, institute=2)

                    try:
                        CollegeAddingStudents.objects.create(
                            selected_course=selected_course, study_center=study_center, name=name, email=email, contact_number=contact_number)
                    except:
                        messages.error(request, "Student not Added, try Again")
                else:
                    messages.error(
                        request, "You've already entered the data of this Student")
                return redirect('study_center:add_student_college')
        context = {
            'title': 'IT Kerala | Add Students',
            'form': form,
            'study_center': study_center,
            'student_added': CollegeAddingStudents.objects.all(),
        }
    else:
        raise Http404
    return render(request, 'college_or_atc/add_student_college.html', context)


@login_required
def college_added_student_verification(request, code):
    context = {
        'title': 'IT Kerala | Student Verification',
    }
    if request.user.user_type == 5 or request.user.user_type == 4:
        study_center = get_object_or_404(StudyCenter, code=code)
        students_added = CollegeAddingStudents.objects.filter(
            study_center__code=code)
        students_pending_approval = CollegeAddingStudents.objects.filter(
            study_center__code=code).filter(verified=False).count()
        context['students_added'] = students_added
        context['study_center'] = study_center
        context['students_pending_approval'] = students_pending_approval

    else:
        raise Http404
    return render(request, 'college_or_atc/verify_and_enroll_students.html', context)


@login_required
def verify_student_added_by_college(request, id):
    # context = {
    #     'title':'IT Kerala | Verification'
    # }
    student = get_object_or_404(CollegeAddingStudents, id=id)
    password = User.objects.make_random_password(
        length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889!@#$%^&*()")
    try:
        user = User.objects.create(name=student.name, email=student.email,
                                   username=student.email, contact_number=student.contact_number)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
    except IntegrityError:
        user = User.objects.get(email=student.email)
        messages.warning(request, "User already exists.")
    try:
        marks = student.selected_course.session_set.count()*4
        Enrollment.objects.create(student=user, college=student.study_center, course=student.selected_course,
                                  assignments_total_obtainable_marks=marks, total_obtainable_marks=marks)
        messages.success(request, "User is now Enrolled")
    except IntegrityError:
        messages.warning(
            request, "User has been previously enrolled for the course")
    send_mail('Credentials - MORE 2019',
              f'Greetings {student.name},\n\nYou have been add to the {student.selected_course} at{student.study_center.name}, {student.study_center.address} These are your login credentials for IT Kerala. \nLogin Email: {student.email}, \nPassword: {password}.\n\nHappy Learning,\n IT Kerala Team', 'noreply@itkeralaedu.com', [student.email], fail_silently=False)
    student.verified = True
    student.save()
    print('\n\nApproved\n\n')
    return redirect('study_center:approve_students_college', student.study_center.code)
