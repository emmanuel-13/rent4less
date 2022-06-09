from django.shortcuts import render, get_object_or_404, redirect

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .models import *
from .forms import PaymentForm
from django.conf import settings
from django.contrib import messages


# Create your views here.
def initiate_payment(request: HttpRequest) -> HttpResponse:
    payments = Payment.objects.all()
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make_payment.html', {
                'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
            })
    else:
        payment_form = PaymentForm()
    return render(request, 'initiate_payment.html', {'payment_form': payment_form, 'payments': payments})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.succcess(request, 'payment verify successfully')
    else:
        messages.error(request, 'verifcation not complete')
    return redirect('payment')