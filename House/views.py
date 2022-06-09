from django.urls import reverse_lazy, reverse
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from .models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.http import HttpResponse
import calendar
from calendar import HTMLCalendar
import csv
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator


def dashboard(request):
    apartment = Estate.objects.all().count()
    user_name = User.objects.filter(is_active=True).count()
    # booking = RoomBooking.objects.all()[:5]
    context = {
        'user_name': user_name, 'estate': apartment
    }
    return render(request, 'Dashboard/dashboard.html', context)


class EstateCreate(SuccessMessageMixin, CreateView):
    model = Estate
    template_name = 'rooms/apartment.html'
    success_message = "estate %(estate)'s created successfully"
    success_url = None
    form_class = EstateForm
    object = None

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        blocks = BlockFormset()
        return self.render_to_response(self.get_context_data(form=form, blocks=blocks))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        blocks = BlockFormset(self.request.POST, instance=form.instance)

        if form.is_valid() and blocks.is_valid():
            return self.form_valid(form, blocks)
        else:
            return self.form_invalid(form, blocks)

    def form_valid(self, form, blocks):
        self.object = form.save(commit=False)
        self.object.save()

        # saving Block Instances
        block = blocks.save(commit=False)
        for aq in block:
            aq.save()

        messages.success(self.request, f'apartment created successfully')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, blocks):
        return self.render_to_response(self.get_context_data(form=form, blocks=blocks))

    def get_success_url(self):
        return reverse_lazy('estate_list')


@staff_member_required
@login_required
def EstateDeleteView(request, pk):
    estate = get_object_or_404(Estate, pk=pk)
    block = Block.objects.filter(estate_names=estate).first()
    apartment = Apartment.objects.filter(block=block, estate_name=estate).all()

    if request.method == "POST":
        estate.delete()
        block.delete()
        apartment.delete()
        if Room.objects.exists():
            room = Room.objects.filter(apartment_name_rooms=estate).all()
            room.delete()
        else:
            pass

        messages.success(request, 'apartment is deleted successfully')
        return redirect('estate_edit')

    context = {
        'estate': estate
    }
    return render(request, 'rooms/apartment_delete.html', context)


class EstateListView(ListView):
    model = Estate
    template_name = 'rooms/apartment_list.html'
    context_object_name = 'estate'
    ordering = ("-estate_name",)


class EstateEdit(ListView):
    model = Estate
    template_name = 'rooms/apartment_edit.html'
    context_object_name = 'estate'


@staff_member_required
@login_required(login_url='login')
def estate_detail(request, estate_name):
    estate = get_object_or_404(Estate, estate_name=estate_name)
    block = Block.objects.filter(estate_names=estate).all()
    # apartment = Apartment.objects.get(block=block, estate_name=estate).count()

    context = {
        'estate': estate, 'block': block
    }
    return render(request, "rooms/apartment_detail.html", context)


@staff_member_required
@login_required(login_url='login')
def block_details(request, estate_id, pk):
    block = get_object_or_404(Block, estate_names_id=estate_id, pk=pk)
    estate = Estate.objects.filter(estate_name=block.estate_names).first()
    apartment = Apartment.objects.filter(estate_name=estate, block=block.block_no).all()

    apartments = Apartment.objects.filter(block=block.block_no, estate_name=estate)
    print(apartments)

    room = Room.objects.all()
    print(room)

    appended = []
    for apart in apartments:
        for rooms in room:
            if apart.flat_id in rooms.flat_id_rooms:
                appended.append(apart.flat_id)

    print(appended)
    context = {
        'apartment': apartment, 'block': block, "estate": estate, 'room': appended
    }

    return render(request, 'rooms/block_details.html', context)


@login_required(login_url='login')
def apartment_room_details(request, flat_id):
    apartment = get_object_or_404(Apartment, flat_id=flat_id)
    estate = Estate.objects.filter(estate_name=apartment.estate_name).first()
    block = Block.objects.all().filter(estate_names=estate)
    # print(apartment.block)

    b = []
    for block in block:
        if apartment.block in block.block_no:
            b.append(block.pk)
    print(b[0])
    room = Room.objects.filter(apartment_name_rooms=apartment.estate_name).all()
    # print(apartment.flat_id)

    new_room = []
    for rooms in room:
        if apartment.flat_id in rooms.flat_id_rooms:
            new_room.append(rooms)

    context = {
        'room': new_room, "apartment": apartment, 'estate': estate, 'b': b[0]
    }

    return render(request, 'rooms/apartment_rooms_detail.html', context)


def apartment_update(request, flat_id):
    apartment = get_object_or_404(Apartment, flat_id=flat_id)
    form = ApartmentForm(instance=apartment)

    estate = Estate.objects.filter(estate_name=apartment.estate_name).first()
    block = Block.objects.all().filter(estate_names=estate)
    # print(apartment.block)

    b = []
    for block in block:
        if apartment.block in block.block_no:
            b.append(block.pk)
    print(b[0])
    room = Room.objects.filter(apartment_name_rooms=apartment.estate_name).all()
    # print(apartment.flat_id)

    new_room = []
    for rooms in room:
        if apartment.flat_id in rooms.flat_id_rooms:
            new_room.append(rooms)

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)

        if form.is_valid():
            form.save()

            messages.success(request, f'apartment {apartment.flat_id} updated successfully')
            return redirect(reverse('block_details', kwargs={'estate_id': estate.id, 'pk': b[0]}))

    context = {
        'form': form, 'apartment': apartment, 'estate': estate, 'b': b[0]
    }

    return render(request, 'rooms/apartment_update.html', context)


def estate_list(request):
    estate_filter = EstateFilter(request.GET, queryset=Estate.objects.all())

    p = Paginator(estate_filter.qs, 5)
    page = request.GET.get('page')
    estates = p.get_page(page)
    context = {
        'filter': estate_filter, 'estates': estates
    }
    return render(request, 'rooms/estate_apartment_list.html', context)


def apartment_list(request, estate_name):
    estate = get_object_or_404(Estate, estate_name=estate_name)
    apartment = Apartment.objects.filter(estate_name=estate)

    if not apartment:
        messages.info(request, f'no apartment found in this estate {estate}')
        return redirect('estate_listing')
    else:
        apartment_filter = ApartmentFilter(request.GET, queryset=apartment)
    
        p = Paginator(apartment_filter.qs, 5)
        page = request.GET.get('page')
        apartments = p.get_page(page)

        context = {
            "apartments": apartments, "myfilter": apartment_filter, 'estate': estate, 'apartment': apartment
        }

        return render(request, 'rooms/estate_list.html', context)


def estate_csv(request):
    response = HttpResponse(content_type="txt/csv")
    response['Content-Disposition'] = 'attachment; filename=estate.csv'

    # creating a csv writer
    writer = csv.writer(response)

    apartment = Estate.objects.all()

    # adding columns
    writer.writerow(['Estate Name', 'City', 'Location', 'Block'])

    for apartment in apartment:
        writer.writerow([apartment.estate_name, apartment.city, apartment.location, apartment.block_set.count()])

    return response


def apartment_csv(request, estate_name):
    response = HttpResponse(content_type="txt/csv")
    response['Content-Disposition'] = 'attachment; filename=apartment.csv'

    # creating a csv writer
    writer = csv.writer(response)

    estate = get_object_or_404(Estate, estate_name=estate_name)
    apartment = Apartment.objects.filter(estate_name=estate.estate_name)

    # adding columns
    writer.writerow(['Block', 'Apartment_Type', 'Flat_id'])

    for apartment in apartment:
        writer.writerow([apartment.block, apartment.flat_types, apartment.flat_id])

    return response


def apartment_test(request, apartment_pk):
    apartment = get_object_or_404(Apartment, pk=apartment_pk)
    estate = Estate.objects.get(estate_name=apartment.estate_name)
    form = ApartmentForm(instance=apartment)

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)

        if form.is_valid():
            form.save()

            messages.success(request, f'room {apartment.flat_id} updated successfully')
            return redirect(reverse('apartment_list', kwargs={'estate_name': estate.estate_name}))

    context = {
        'form': form, 'apartment': apartment, 'estate': estate
    }
    return render(request, 'rooms/apartment_test.html', context)


@login_required(login_url='login')
def apartment_room_test(request, flat_id):
    apartment = get_object_or_404(Apartment, flat_id=flat_id)
    estate = Estate.objects.get(estate_name=apartment.estate_name)

    room = Room.objects.filter(apartment_name_rooms=apartment.estate_name).all()
    # print(apartment.flat_id)

    new_room = []
    for rooms in room:
        if apartment.flat_id in rooms.flat_id_rooms:
            new_room.append(rooms)

    context = {
        'room': new_room, "apartment": apartment, 'estate': estate
    }

    return render(request, 'rooms/apartment_room_test.html', context)


def room_update(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)

        if form.is_valid():
            form.save()

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect(reverse('apartment_room_test', kwargs={'flat_id': room.flat_id_rooms}))

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_create_update.html', context)


def room_detail(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    context = {
        "room": room
    }
    return render(request, 'rooms/room_detail.html', context)


def room_detail_main(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    context = {
        "room": room
    }
    return render(request, 'rooms/room_main_detail.html', context)


def room_list(request):
    room = Room.objects.all()
    myfilter = RoomFilter(request.GET, queryset=room)
    context = {
        'room': room, 'myfilter': myfilter
    }
    return render(request, 'rooms/room_list.html', context)


def room_update_2(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)

        if form.is_valid():
            form.save()

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect("room_list")

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_update.html', context)

