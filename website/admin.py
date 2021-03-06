from django.contrib import admin

# Register your models here.
from .models import (
    Category, Subcategory, Event, EventPhotos, EventFile,
    Organization, Customer, Trip, Quote, Testimonial,
    TripPhoto, TripFile, ContactRequest
)


class EventPhotosInline(admin.TabularInline):
    model = EventPhotos


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'caption', 'rank', 'updated', 'timestamp']


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'caption', 'rank', 'updated', 'timestamp']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'zip', 'updated', 'timestamp']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'occupation', 'email', 'phone_number', 'updated', 'timestamp']


class TripPhotosInline(admin.TabularInline):
    model = TripPhoto


class TripFilesInline(admin.TabularInline):
    model = TripFile


class EventFilesInline(admin.TabularInline):
    model = EventFile


class TripAdmin(admin.ModelAdmin):
    inlines = [TripPhotosInline, TripFilesInline]
    list_display = ['title', 'destination', 'date', 'updated', 'timestamp']


class EventAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline, EventFilesInline]
    list_display = ['title', 'date', 'updated', 'timestamp']


class QuoteAdmin(admin.ModelAdmin):
    # TODO: improve admin display
    list_display = ['email', 'first_name', 'last_name', 'date', 'transportation', 'preferred_airport']


class TestimonialAdmin(admin.ModelAdmin):
    # TODO: improve admin display
    list_display = ['full_name', 'organization', 'trip', 'event', 'date']


class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(ContactRequest, ContactRequestAdmin)
