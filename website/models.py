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


