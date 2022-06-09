from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(OrderItem)
admin.site.register(Order)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject']
