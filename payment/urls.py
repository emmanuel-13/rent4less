from django.urls import path
from .views import *

urlpatterns = [
    path('payment/', initiate_payment, name='payment'),
    path('<str:ref>/', verify_payment, name='verify_payment'),
]
