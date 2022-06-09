from cgitb import lookup
from django import forms
from .models import *
from django.forms import inlineformset_factory
import django_filters
from django.forms import ClearableFileInput


class EstateForm(forms.ModelForm):
    
    class Meta:
        model = Estate
        exclude = ()


BlockFormset = inlineformset_factory(
    Estate, Block, extra=1, fields="__all__", can_delete=False, max_num=5
)


# ApartmentImageFormset = inlineformset_factory(
#     Apartment, ApartmentImage, form=ApartmentForm, fields="__all__", extra=1, can_delete=False
# )

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ("apartment_type", "bedroom_type", "apartment_image")


class ApartmentFilter(django_filters.FilterSet):
    block = django_filters.AllValuesFilter()
    flat_id = django_filters.AllValuesFilter()
    apartment_type = django_filters.AllValuesFilter()

    class Meta:
        model = Apartment
        fields = ["flat_id"]


class RoomFilter(django_filters.FilterSet):
    apartment_name_rooms = django_filters.AllValuesFilter(lookup_expr='exact')
    blocks = django_filters.AllValuesFilter()
    room_id = django_filters.AllValuesFilter()

    class Meta:
        model = Room
        fields = ["apartment_name_rooms"]


class EstateFilter(django_filters.FilterSet):
    estate_name = django_filters.AllValuesFilter(lookup_expr='exact')
    location = django_filters.AllValuesFilter()
    city = django_filters.AllValuesFilter()

    class Meta:
        model = Estate
        fields = ["city"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("room_types", "capacity", "ammenities", "image1", "rent", "service_charge", "power_charge")
        

class ApartmentLevel(forms.ModelForm):
    apartment_type = django_filters.AllValuesFilter()
    
    class Meta:
        model = Apartment
        fields = ['bedroom_type']
        
        
        

