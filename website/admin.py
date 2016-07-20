from django.contrib import admin

# Register your models here.
from .models import (
    EventCategory, Event, EventPhotos,
    Organization, Customer, Trip, Quote, Testimonial
)


class EventPhotosInline(admin.TabularInline):
    model = EventPhotos


class EventAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline]
    list_display = ['title', 'date', 'category', 'updated', 'timestamp']


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'caption', 'updated', 'timestamp']


admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Event, EventAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'zip', 'updated', 'timestamp']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'occupation', 'email', 'phone_number', 'updated', 'timestamp']
class TripAdmin(admin.ModelAdmin):
    list_display = ['type', 'destination', 'date', 'draft', 'updated', 'timestamp']


class QuoteAdmin(admin.ModelAdmin):
    # TODO: improve admin display
    list_display = ['travelers', 'transportation', 'preferred_airport']


class TestimonialAdmin(admin.ModelAdmin):
    # TODO: improve admin display
    list_display = ['text']

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Testimonial, TestimonialAdmin)

