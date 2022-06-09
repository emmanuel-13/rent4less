from django.contrib.auth.models import User
from django import forms

from .models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city']
