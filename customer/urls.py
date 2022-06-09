from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('login/', login_attempt, name='login'),
    path('register/', register_attempt, name='register'),
    path('success/', success_attempt, name='success'),
    path('token/', token_send, name='token'),
    path('verify/<auth_token>/', verify, name='verify'),
    path('error/', token_send, name='error'),
    path('logout/', logout_request, name='logout'),
    path('contact/', contact, name="contact"),

    #user dasboard
    path('user/dashboard', user_dashboard, name="user_dashboard"),
    path('user/bookings', user_bookings, name="user_booking"),

    #home page
    path('property/', property, name="property"),
    path('property/<pk>', property_details, name='property_detail'),
    # path('property/estate_name/<id>/', estate_details, name='estate_detail'),
    path('property/<estate_pk>/estate', apartment_details, name='apartment_detail'),
    path('property-rooms/<pk>/rooms', property_room, name='property_rooms'),
    path('about/', about, name="about"),
    path('city/', city, name="city"),

    #function ajax
    path('estate_listing', EstateListAjax, name="estate-listing"),
    path('search', search, name="estate-search"),
    
    #checkout
    path('order/',customer_order,name='order')

]
