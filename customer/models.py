from django.contrib.auth.models import User
from django.db import models
from House.models import *


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.subject


class RoomCart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quantity = models.CharField(default=0, max_length=1)

    def __str__(self):
        return self.user.username
    
    
class Order(models.Model):
    customer_username  =  models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = (
        ('Pending', 'Pending'), ('Paid', 'Paid')
    )
    payment_status = models.CharField(max_length=20, choices=status, default="Pending")
    
    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self):
        return f'Order {self.id} by {self.first_name}'
    
    
    def get_total_cost(self):
            return sum(room.get_cost() for room in self.room.all())
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                                  related_name='items',
                                  on_delete=models.CASCADE)
    room = models.ForeignKey(Room,
                                 related_name='order_room',
                                 on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    # ordered_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
            return str(self.id)

    def get_cost(self):
        return self.price