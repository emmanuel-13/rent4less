from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('estate_create/', EstateCreate.as_view(), name="estate_create"),
    path('estate_list/', EstateListView.as_view(), name="estate_list"),
    path('<estate_name>/', estate_detail, name='estate_detailing'),
    path('estate_edit/edit', EstateEdit.as_view(), name='estate_edit'),
    path('estate_delete/<pk>', EstateDeleteView, name='estate_delete'),
    path('<estate_id>/<pk>', block_details, name='block_details'),

    #apartment
    path('rooms/<flat_id>/', apartment_room_details, name='room_det'),
    path('<flat_id>/apartment_update/', apartment_update, name='apartment_update'),
    path('apartment/<estate_name>/', apartment_list, name='apartment_list'),
    path('apartment/estate_csv/myestatecsv', estate_csv, name='estate_csv'),
    path('apartment/apartment_csv/<estate_name>', apartment_csv, name='apartment_csv'),
    path('apartment/estate_list/estate-apartment', estate_list, name='estate_listing'),

    #testing apartment
    path('<apartment_pk>/apartment_testing/', apartment_test, name='apartment_test'),
    path('apartment/<flat_id>/apartd', apartment_room_test, name='apartment_room_test'),

    #rooms
    path('rooms/<room_id>/rooms', room_update, name='room_update'),
    path('rooms/<room_id>/rooms_detail', room_detail, name='room_detail'),
    path('rooms/<room_pk>/rooms_detail_main', room_detail_main, name='room_details'),
    path('rooms/rooms_update/<room_pk>', room_update_2, name='room_detail_update'),
    path('\\room', room_list, name='room_list'),
]