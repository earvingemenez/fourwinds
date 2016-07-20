from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver


def get_path(instance, filename, path):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(path, filename)


def get_event_photos_path(instance, filename):
    return get_path(instance, filename, 'events')


def get_quotes_files_path(instance, filename):
    return get_path(instance, filename, 'quotes')


class EventCategory(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=100)
    caption = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title


class Event(models.Model):

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class EventPhotos(models.Model):

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    photo = models.ImageField(upload_to=get_event_photos_path,
                              null=False,
                              blank=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


@receiver(post_delete, sender=EventPhotos)
def event_photo_delete(sender, instance, **kwargs):
    instance.photo.delete(False)


class Organization(models.Model):
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    name = models.CharField(max_length=100)
    # Schools only
    education_department = models.CharField(max_length=100)
    # End Schools only
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

    type = models.CharField(max_length=100)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    draft = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.destination


class Quote(models.Model):
    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"

    travelers = models.IntegerField()
    # Schools only
    grade_levels = models.CharField(max_length=50)
    complementary_chaperones = models.IntegerField()
    # End Schools only
    transportation = models.CharField(max_length=150)
    preferred_airport = models.CharField(max_length=200)
    meals_to_include = models.CharField(max_length=60)
    budget = models.CharField(max_length=200)
    reference_file = models.FileField(
        upload_to=get_quotes_files_path,
        null=True,
        blank=False)
    how_hear = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class Testimonial(models.Model):
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    text = models.TextField(null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

