from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.db.models import Func
from django.dispatch.dispatcher import receiver
from django.utils import timezone


class Month(Func):
    def __ror__(self, other):
        pass

    def __rand__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Year(Month):
    template = '%(function)s(YEAR from %(expressions)s)'


def get_path(instance, filename, path):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(path, filename)


def get_event_photos_path(instance, filename):
    return get_path(instance, filename, 'events')


def get_quotes_files_path(instance, filename):
    return get_path(instance, filename, 'quotes')


def get_trip_photos_path(instance, filename):
    return get_path(instance, filename, 'trips/photos')


def get_trip_pdf_path(instance, filename):
    return get_path(instance, filename, 'trips/pdf')


def get_category_bg_path(instance, filename):
    return get_path(instance, filename, 'categories')


class Category(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=100, default="General")
    caption = models.TextField(blank=True)
    widget_top_bg = models.ImageField(upload_to=get_category_bg_path, null=False, blank=False, default='')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def events(self):
        return self.event_set.all()[:10]


class Event(models.Model):

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def photos(self):
        return self.eventphotos_set.all()[:10]


class EventPhotos(models.Model):

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    photo = models.ImageField(upload_to=get_event_photos_path, null=False, blank=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Organization(models.Model):
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="United States")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    phone_ext = models.CharField(max_length=10, null=True, blank=True)
    contact_method = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Trip(models.Model):

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    type = models.CharField(max_length=100)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    draft = models.BooleanField(default=True)
    start_location = models.CharField(max_length=255, default='')
    end_location = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.destination

    @property
    def photos(self):
        return self.tripphoto_set.all()[:10]


class TripPhoto(models.Model):

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    photo = models.ImageField(upload_to=get_trip_photos_path,
                              null=False,
                              blank=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class TripFile(models.Model):

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    file = models.FileField(upload_to=get_trip_pdf_path,
                             null=False,
                             blank=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Quote(models.Model):
    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    phone_ext = models.CharField(max_length=10, null=True, blank=True)
    organization_name = models.CharField(max_length=150)
    organization_zip = models.CharField(max_length=50)
    trip_type = models.CharField(max_length=100)
    number_students = models.IntegerField()
    destination = models.CharField(max_length=250)
    date = models.DateField(default=timezone.now())
    budget = models.CharField(max_length=150)
    notes = models.TextField(blank=True, default='')
    # optional fields
    followup_time = models.CharField(blank=True, default='', max_length=50)
    chaperones = models.IntegerField(blank=True, null=True)
    department = models.CharField(blank=True, null=True, default='', max_length=100)
    transportation = models.CharField(blank=True, null=True, default='', max_length=100)
    preferred_airport = models.CharField(blank=True, null=True, default='', max_length=100)
    meal_to_include = models.CharField(blank=True, null=True, default='', max_length=100)
    attachment = models.FileField(upload_to=get_quotes_files_path, null=True, blank=True, default='')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class Testimonial(models.Model):
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    text = models.TextField(null=False, blank=False)
    full_name = models.CharField(max_length=150, default='')
    organization = models.CharField(max_length=150)
    trip = models.CharField(max_length=150, default='', null=True, blank=True)
    event = models.CharField(max_length=150, default='', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __repr__(self):
        return self.full_name


class Receivers:
    @staticmethod
    @receiver(post_delete, sender=EventPhotos)
    def event_photo_delete(sender, instance, **kwargs):
        instance.photo.delete(False)

    @staticmethod
    @receiver(post_delete, sender=TripPhoto)
    def trip_photo_delete(sender, instance, **kwargs):
        instance.photo.delete(False)

    @staticmethod
    @receiver(post_delete, sender=TripFile)
    def trip_file_delete(sender, instance, **kwargs):
        instance.photo.delete(False)


class ContactRequest(models.Model):
    class Meta:
        verbose_name = 'Contact Request'
        verbose_name_plural = 'Contact Requests'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    date = models.DateField(blank=True, default='')
    organization = models.CharField(blank=True, default='', max_length=200)
    message = models.TextField()
    newsletter = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
