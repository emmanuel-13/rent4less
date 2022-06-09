from requests import request
from House.models import *
from House.forms import ApartmentLevel
from django import template
from django.shortcuts import render


register = template.Library()


@register.simple_tag(name='my_apartment')
def my_contacts():
    apartments = Apartment.objects.all().last()
    room = Room.objects.filter(flat_id_rooms=apartments.flat_id)
    
    return room