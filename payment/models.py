import email
from django.db import models
import secrets
from .paystack import Paystack
from customer.models import OrderItem, UserProfile



class Payment(models.Model):
    orderitem = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f"Payment of: #{self.orderitem.price}- made by {self.email}"

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.orderitem.price * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.orderitem.price)
        if status:
            if result['self.orderitem.price'] / 100 == self.orderitem.price:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
