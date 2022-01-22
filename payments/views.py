from django.core.mail import send_mail
from courses.models import Enrollment
from django.contrib.auth.decorators import login_required
from payments.models import Order
from accounts.models import User
from college_or_atc.models import StudyCenter
from django.shortcuts import redirect, render
import razorpay
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from cart.models import StudentAdded, StudentCart, StudyCenterCart
from django.db import IntegrityError

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@login_required
def payment(request):
    currency = 'INR'
    amount = 100
    user = request.user
    if request.user.user_type == 1:
        price = StudentCart.objects.get(user=request.user).price
    elif request.user.user_type == 2 or request.user.user_type == 4 or request.user.user_type == 5:
        student_cart = StudentCart.objects.get(user=request.user)
        if not Enrollment.objects.filter(student=student_cart.user).filter(course=student_cart.course):
            marks = student_cart.course.session_set.count()*4
            Enrollment.objects.create(student=student_cart.user, college=student_cart.college,course=student_cart.course, assignments_total_obtainable_marks=marks, total_obtainable_marks=marks)
        student_cart.delete()
        return redirect('courses:enrolled_courses')
    else:
        price = StudyCenterCart.objects.get(study_center_admin_user=request.user).price
        # Amount is taken in Rupees in side model. Therefore multiplied by 100 to convert to Paisa for Razorpay
        # Amount should always be passed as an Integer.
    amount = int(price*100)
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(
        dict(amount=int(amount), currency=currency, payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/payment-handler/'
    # we need to pass these details to frontend.
    context = {'title': 'IT Kerala | Fee Payment'}
    if request.user.user_type == 3:
        context['students'] = StudentAdded.objects.filter(
            college=StudyCenter.objects.get(admin_user=request.user)).filter(fee_paid=False)
    else:
        context['student'] = StudentCart.objects.get(user=request.user)
    context['amount'] = amount/100
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['contact'] = user.contact_number
    context['email'] = user.email
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'payment_gateway/payment_index.html', context=context)

# we need to csrf_exempt this url as POST request will be made by Razorpay and it won't have the csrf token.


@csrf_exempt
@login_required
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature}
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is None:
                if request.user.user_type == 1 or request.user.user_type == 5 or request.user.user_type == 2:
                    price = StudentCart.objects.get(user=request.user).price
                else:
                    study_center_cart = StudyCenterCart.objects.get(study_center_admin_user=request.user)
                    price = StudyCenterCart.objects.get(study_center_admin_user=request.user).price
                amount = int(price*100)
                try:
                    order = Order.objects.create(user=request.user, total_amount=amount, payment_status=1, datetime_of_payment=timezone.now(
                    ), razorpay_order_id=razorpay_order_id, razorpay_payment_id=payment_id, razorpay_signature=signature)
                    order.save()
                    if request.user.user_type == 3:
                        study_center_cart.delete()
                        students = StudentAdded.objects.filter(college=StudyCenter.objects.get(
                            admin_user=request.user)).filter(fee_paid=False)
                        for student in students:
                            marks = student.course.session_set.count()*4
                            if not Enrollment.objects.filter(student=student.user).filter(course=student.course):
                                Enrollment.objects.create(student=student.user, college=student.college, course=student.course, assignments_total_obtainable_marks=marks, total_obtainable_marks=marks)
                        StudentAdded.objects.filter(college=StudyCenter.objects.get(
                            admin_user=request.user)).update(fee_paid=True, order=order)
                        study_center_cart.delete()
                    else:
                        student_cart = StudentCart.objects.get(user=request.user)
                        marks = student_cart.course.session_set.count()*4
                        if not Enrollment.objects.filter(student=student_cart.user).filter(course=student_cart.course):
                            marks = student_cart.course.session_set.count()*4
                            Enrollment.objects.create(student=student_cart.user, college=student_cart.college,
                                                            course=student_cart.course, assignments_total_obtainable_marks=marks, total_obtainable_marks=marks)
                        try:
                            student_cart.delete()
                        except:
                            pass
                        send_mail('Credentials - MORE 2019',
                                  f'Greetings,\n\n Mr. {student_cart.user.name} has registered for {student_cart.course.course_name} at {student_cart.college.name}. \nStudent Email: {student_cart.user.email}, \nContact Number: {student_cart.user.contact_number}.\n\nIT Kerala Team', 'noreply@itkeralaedu.com', [student_cart.college.admin_user.email], fail_silently=False)
                    # capture the payment
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return render(request, 'payment_gateway/paymentsuccess.html')
                except:
                    Order.objects.create(user=request.user, total_amount=amount, payment_status=2, datetime_of_payment=timezone.now(
                    ), razorpay_order_id=razorpay_order_id, razorpay_payment_id=payment_id, razorpay_signature=signature)
                    # if there is an error while capturing payment.
                    return render(request, 'payment_gateway/paymentfail.html')
            else:
                # if signature verification fails.
                return render(request, 'payment_gateway/paymentfail.html')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
