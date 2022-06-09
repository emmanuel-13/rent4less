import requests
import json 

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from House.models import *
from .cart import Cart

def cart_display(request):
	cart = Cart(request)
	carts = cart.list()
	context = {
		'cart':cart
	}
	return render(request,'cart.html',context)

	'''
[
   {
      "id":"3",
      "obj":"<Product":"Java Programming>",
      "quantity":8.0,
      "price":"Decimal("      "27640"      ")"
   },
   {
      "id":"2",
      "obj":"<Product":"Python Programming>",
      "quantity":1,
      "price":"Decimal("      "1500"      ")"
   },
   {
      "id":"1",
      "obj":"<Product":"Tshory>",
      "quantity":1,
      "price":"Decimal("      "500"      ")"
   }
]
	'''


def add_to_cart(request,id):
    print(request.session.get("room_cart"))
    room = Room.objects.get(id=id)
    apartment = Apartment.objects.get(flat_id=room.flat_id_rooms)
    estate = Estate.objects.get(estate_name=room.apartment_name_rooms)
    cart = Cart(request)
    cart.add(room)
    room.active = True
    room.save()
    messages.success(request, f'room {room} added to your booking please proceed to your booking to checkout')
    return redirect(reverse("apartment_detail", kwargs={'estate_pk': estate.pk }))


def delete_cart(request,id):
   cart = Cart(request)
   cart.delete(id)
   room = get_object_or_404(Room, id=id)
   apartment = Apartment.objects.get(flat_id=room.flat_id_rooms)
   
   context = {
            'cart':cart, 'apartment': apartment
         }
   return render(request,'cart.html',context)