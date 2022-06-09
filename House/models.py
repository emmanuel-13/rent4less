from email.policy import default
from django.db import models
import re
from PIL import Image
from django.urls import reverse


class City(models.Model):
    
    citys = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='city', blank=True, null=True)
    status = models.CharField(default=0, editable=False, max_length=1)

    def __str__(self):
        return self.citys


class Estate(models.Model):
    estate_name = models.CharField(max_length=100, unique=True, help_text="enter a valid apartment name",)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True, default="download_6mOeWlD.jfif")
    city = models.CharField(max_length=20)
    location = models.CharField(max_length=40)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.estate_name

    def estate_names(self):
        return self.estate_name

    def estate_delete(self):
        if Estate.objects.delete():
            Block.objects.filter(estate_names=self.estate_name)
            Apartment.objects.filter(estate_name=self.estate_name)
            Room.objects.filter(apartment_name_rooms=self.estate_name)
        else:
            pass

    def new_apartment_name(self):
        apartment = self.estate_name
        apartment = str(apartment)

        apartment = re.split('\s+', apartment)

        new = []
        for new_apartment in apartment:
            if len(new_apartment) >= 1:
                new_apartment = new_apartment[0]
                new.append(new_apartment)

        new = "".join(new)
        new = new.upper()
        return new

    def save(self, *args, **kwargs):
        self.new_apartment_name
        self.estate_name
        self.image = self.image
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        
        if img.height > 450 and img.width > 500:
            output_size = (450, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name_plural = "Estates"
        ordering = ("estate_name",)

    def get_absolute_url(self):
        return reverse("block_details", kwargs={"estate_names_id": self.estate_id, 'pk': self.pk})


class Block(models.Model):
    estate_names = models.ForeignKey(Estate, on_delete=models.CASCADE)
    block_no = models.CharField(max_length=2, null=False, blank=False)
    total_flat = models.CharField(max_length=10, null=True, blank=False)

    def __str__(self):
        return self.block_no

    @property
    def total_flat_no(self):
        return self.total_flat

    def save(self, *args, **kwargs):
        self.total_flat_no

        apartment = self.estate_names
        apartments = str(apartment)

        apartments = re.split('\s+', apartments)

        new = []
        for new_apartments in apartments:
            if len(new_apartments) >= 1:
                new_apartments = new_apartments[0]
                new.append(new_apartments)

        new = "".join(new)
        new = new.upper()

        total_flats = int(self.total_flat)

        triple = []
        for i in range(1, (total_flats) + 1):
            signle = new + self.block_no + "|" + str(i)
            triple.append(signle)

        values = triple

        apart = []

        for i in values:
            estate_name = self.estate_names
            block = self.block_no
            location = self.estate_names.location
            city = self.estate_names.city
            flat = i
            apart.append(Apartment(estate_name=estate_name, block=block, flat_id=flat))

        Apartment.objects.bulk_create(apart)
        super().save(*args, **kwargs)


class Apartment(models.Model):
    types = (
        ('S', 'Shared Apartment'), ('X', 'Exclusive Apartment')
    )

    flat_types = (
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
    )

    estate_name = models.CharField(max_length=20, null=True, blank=True)
    block = models.CharField(max_length=20, null=True, blank=True)
    flat_id = models.CharField(max_length=20, null=True, blank=True)
    apartment_type = models.CharField(max_length=20, choices=types, default=[0][0])
    bedroom_type = models.CharField(max_length=20, choices=flat_types)
    apartment_image = models.ImageField(upload_to='apartment/', null=True)

    def __str__(self):
        return self.flat_id

    class Meta:
        ordering = ("flat_id",)

    def save(self, *args, **kwargs):

        flat_id = self.flat_id

        room = int(self.bedroom_type)

        rooms = []
        for room in range(1, room+1):
            new_list = flat_id + '|' + str(room)
            rooms.append(new_list)

        roomsss = Room.objects.filter(flat_id_rooms=flat_id).all()

        room_list = []
        for room in rooms:
            room_list.append(Room(apartment_name_rooms=self.estate_name, blocks=self.block, 
                                  flat_id_rooms=self.flat_id, room_id=room, apartment_type=self.apartment_type,
                                  bedroom_type=self.bedroom_type))

        if Room.objects.exists():
            roomsss.delete()
            Room.objects.bulk_create(room_list)
        else:
            Room.objects.bulk_create(room_list)
        super().save(*args, **kwargs)


class Room(models.Model):
    type_rooms = (
        ('Executives', 'executives'), ('Standard', 'standard'), ('Mini', 'mini'), ('Deluxe', 'deluxe')
    )

    status = (
        ('available', 'available'), ('expired', 'expired'), ('terminated', 'terminated'), ('running', 'running')
    )
    
    types = (
        ('S', 'Shared Apartment'), ('X', 'Exclusive Apartment')
    )

    flat_types = (
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    )

    apartment_name_rooms = models.CharField(max_length=50, null=True, blank=True, editable=False)
    blocks = models.CharField(max_length=10, null=True, blank=True, editable=False)
    flat_id_rooms = models.CharField(max_length=10, null=True, blank=True, editable=False)
    apartment_type = models.CharField(max_length=20, choices=types, default=[0][0], editable=False)
    bedroom_type = models.CharField(max_length=20, choices=flat_types)
    room_id = models.CharField(max_length=20, null=True, blank=True)
    room_types = models.CharField(max_length=15, null=False, blank=False, choices=type_rooms)
    capacity = models.SmallIntegerField(default=0)
    ammenities = models.TextField()
    image1 = models.FileField(upload_to='uploads/post_photos', blank=True, null=True)
    unique_room_id = models.CharField(max_length=20, null=True, editable=True, blank=True)
    rent = models.FloatField()
    service_charge = models.FloatField()
    power_charge = models.FloatField()
    price = models.FloatField(editable=False)
    occupied = models.CharField(default="available", choices=status, max_length=10)
    active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Room'
        abstract = False
        ordering = ("apartment_name_rooms",)

    def room_save(self):
        return self.occupied

    def room_occupied(self):
        return self.occupied

    def save(self, *args, **kwargs):
        self.unique_room_id = self.room_id + self.room_types[0]
        self.unique_room_id
        self.price = self.rent + self.service_charge + self.power_charge
        self.price
        self.occupied
        self.room_save
        

        super().save(*args, **kwargs)

    def __str__(self):
        return self.flat_id_rooms


class Testemonial(models.Model):
    name = models.CharField(max_length=20)
    content = models.TextField()
    images = models.ImageField(upload_to='testemonials', null=True, blank=True)

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.images.path)

        if img.height > 450 and img.width > 500:
            output_size = (450, 500)
            img.thumbnail(output_size)
            img.save(self.images.path)

