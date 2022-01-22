from courses.models import Course
from accounts.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class Order(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE'),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()

    payment_status = models.IntegerField(
        choices=payment_status_choices, default=3)

    datetime_of_payment = models.DateTimeField(default=timezone.now)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.order_id is None and self.datetime_of_payment and self.id:
    #         self.order_id = self.datetime_of_payment.strftime(
    #             'PAY2ME%Y%m%dODR') + str(self.id)
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email} - Razorpay ID: {self.razorpay_order_id} -- Amount: Rs. {self.total_amount}'


# class ProductInOrder(models.Model):
#     class Meta:
#         unique_together = (('order', 'product'),)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Course, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.FloatField()
