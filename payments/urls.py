from django.urls import path
from payments.views import payment, paymenthandler

app_name = 'payment_gateway'
urlpatterns = [
    path('payment/', payment, name='payment'),
    path('payment-handler/', paymenthandler, name='paymenthandler'),
]
