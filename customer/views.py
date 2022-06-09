from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password

from django.contrib import messages
from datetime import datetime, date, timedelta
import random
from House.forms import *
from House.models import *

# Own imports
from customer.models import *
from House.models import *
from .forms import *
from django.db.models import Q
from cart.cart import Cart
from django.core.paginator import Paginator



def home(request):
    city = City.objects.all()[:8]
    estate = Estate.objects.all()[:4]
    testemonial = Estate.objects.filter(is_featured=True).all()
    apartment = Apartment.objects.filter(apartment_type="X")[:3]

    context = {
        'city': city, 'estate': estate, 'testemonial': testemonial, 'apartment': apartment
    }
    return render(request, 'index.html', context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('content')
            messages.success(request, 'infomation send successfully')
            send_mail_user(email, subject)
            return redirect('contact')
        else:
            messages.error(request, 'invalid credentials')
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


def send_mail_user(email, subject):
    subject = "Automated Machine on this Platform"
    message = f'hi {email} we have receive your mail on the subject {subject} and we would get back to you as soon as possible for futher informations please to well to reach out to us on the following lines 09161444754'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject, message, email_from, recipient_list)


@login_required(login_url='login')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    user_first = User.objects.all().get(id=request.user.id)
    user = UserProfile.objects.get(user=user_first)
    print(f"request user id ={request.user.id}")

    return render(request, 'mybookings.html')


@login_required(login_url='login')
def user_dashboard(request):
    user_first = User.objects.all().get(id=request.user.id)
    user = UserProfile.objects.get(user=user_first)
    print(f"request user id ={request.user.id}")
    return render(request, 'user_dashboard.html', {
        'users': user
    })


# def handler404(request, exception):
#     return render(request, '404.html', status=404)
#
#
# def history(request):
#     try:
#         booking = RoomBooking.objects.get(request.session["booking"])
#     except (KeyError, RoomBooking.DoesNotExist):
#         booking = None
#     return render(request, 'user_history.html', {'booking': booking})


from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, logout, login


# Create your views here.
def login_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'username don\'t exists')
            return redirect('login')

        profile_obj = UserProfile.objects.filter(user=user_obj).first()
        if profile_obj.is_verified is None:
            messages.success(request, 'profile is not verified, please check your mail')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, 'username or password incorrect')
            return redirect('login')

        login(request, user)
        return redirect('home')

    return render(request, 'login.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def register_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'username is taken')
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'email is taken')
                return redirect('register')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            print(auth_token)
            profile_obj = UserProfile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            send_mail_register(email, auth_token)
            return redirect('token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')


def verify(request, auth_token):
    try:
        profile_obj = UserProfile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Email Already verified')
                return redirect('login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Email verified please login')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)


def error(request):
    return render(request, 'error.html')


@login_required(login_url="login")
def success_attempt(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token.html')


def send_mail_register(email, token):
    subject = "your account needs to be verified"
    message = f'hi  {email}, please click the link to verify your email http://127.0.0.1:8000/customer/verify/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject, message, email_from, recipient_list)


def property(request):
    estate_list = Estate.objects.all()

    context = {
        'estate': estate_list
    }
    return render(request, 'property-grid.html', context)


def property_details(request, pk):
    city = get_object_or_404(City, pk=pk)
    estate = Estate.objects.filter(city=city)
    city_list = City.objects.all()[:6]
    
    citys = City.objects.filter(status=0).values_list('citys', flat=True)
    citys = list(citys)

    if estate:
        pass
    else:
        messages.info(request, "no estate in that location please try another city")
        return redirect('home')

    context = {
        'estate': estate, 'city': city, 'city_list': city_list
    }
    return render(request, 'listing.html', context)


import json

def apartment_details(request, estate_pk):
    estate = get_object_or_404(Estate, pk=estate_pk)
    room = Room.objects.filter(apartment_name_rooms=estate.estate_name)
    apartment = Apartment.objects.filter(estate_name=estate.estate_name)[:4]
    city = City.objects.get(citys=estate.city)

    print(estate)
    

    if room:
        pass
    else:
        messages.info(request, "no room availabe here")
        return redirect(reverse('property_detail', kwargs={'pk': city.pk }))
    

    context = {
        'room': room, "estate": estate, 'city': city, 'apartment': apartment
    }
    return render(request, 'single.html', context)


def property_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    apartment = Apartment.objects.get(flat_id=room.flat_id_rooms)
    estate = Estate.objects.get(estate_name=apartment.estate_name)
    city = City.objects.get(citys=estate.city)

    context = {
        'room': room, 'apartment': apartment, 'estate': estate, 'city': city
    }
    return render(request, 'property_room.html', context)


def about(request):
    context = {

    }
    return render(request, 'about.html', context)


def city(request):
    city = City.objects.all()
    return render(request, 'city.html', {'city': city})

def EstateListAjax(request):
    city = City.objects.filter(status=0).values_list('citys', flat=True)
    citylist = list(city)

    return JsonResponse(citylist, safe=False)


def search(request):
    if request.method == "POST":
        city_search = request.POST.get('search')

        if city_search == "":
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            city = City.objects.filter(citys__icontains=city_search).first()

            if city:
                return redirect("property/"+str(city.pk))
            else:
                messages.info(request, 'no property matches your search')
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))
    

def customer_order(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            order = form.save()
            total_carts = cart.list()
            for c in total_carts:
                print(c)
                obj,created =  OrderItem.objects.get_or_create(
                    order=order,
                    defaults={
                    'room': c['obj']
                })
            if obj:
                cart.clearcart()
                # html_to_pdf_view(obj.id)
                return redirect('payment')
    else:
                
        form = OrderCreateForm()
    
    context = {
        'form':form,
        'cart':Cart(request)
    }
    return render(request,'order.html',context)