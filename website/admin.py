from django.contrib import admin

# Register your models here.
from .models import EventCategory, Event, EventPhotos


class EventPhotosInline(admin.TabularInline):
    model = EventPhotos


class EventAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline]
    list_display = ['title', 'date', 'category', 'updated', 'timestamp']


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'caption', 'updated', 'timestamp']

admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Event, EventAdmin)

