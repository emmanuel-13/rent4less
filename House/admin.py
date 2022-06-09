from django.contrib import admin
from .models import *


class BlockInline(admin.StackedInline):
    model = Block
    extra = 1


admin.site.register(City)


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ['estate_name', 'location', 'new_apartment_name', 'date_added']
    search_fields = ['city']
    inlines = [BlockInline]


@admin.register(Apartment)
class Apartment(admin.ModelAdmin):
    list_display = ['estate_name', 'block', 'flat_id', 'apartment_type', 'bedroom_type']
    list_filter = ['flat_id', 'apartment_type']
    list_per_page = 10

    fieldsets = (
        ("", {
            "fields": (
                ['estate_name', 'block', 'flat_id', 'apartment_type', 'bedroom_type', 'apartment_image']
            ),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['estate_name', 'block', 'flat_id']
        else:
            return []

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['apartment_name_rooms', 'blocks', 'flat_id_rooms', 'room_id', 'unique_room_id', 'room_types', 'price', 'occupied']
    fieldsets = (
        ("Room", {
            "fields": (
                ['apartment_name_rooms', 'blocks', 'room_id', 'room_types', 'ammenities', 'image1', 'rent', 'service_charge', 'power_charge',
                 'occupied', 'capacity', 'active']
            ),
        }),
    )
    list_editable = ['occupied']
    list_filter = ['room_id', 'room_types', 'price']
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['blocks', 'room_id', 'apartment_name_rooms']
        else:
            return []

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Testemonial)
