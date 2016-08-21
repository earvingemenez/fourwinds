import re
from datetime import date, datetime
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import Concat
from website.models import Trip, Event, Category, Testimonial, Month, Year, ContactRequest


def index(request):
    return render(request, 'website/index.html')


def our_story(request):
    return render(request, 'website/our-story.html')


def category_travels(request, category_id):
    category = Category.objects.get(id=category_id)
    trips = Trip.objects.filter(category=category)
    events = Event.objects.filter(category=category)
    return render(request, 'website/travels.html', context={'trips': trips, 'events': events, 'category': category})


def map_months_counter(row):
    m = re.search('([0-9]{4})([0-9]{1,2})', str(row['year_month']))
    mdate = date(int(m.group(1)), int(m.group(2)), 1)
    row['year_month'] = mdate.strftime('%Y-%m')
    row['date'] = mdate.strftime('%B, %Y')
    return row


def travel(request, year_month=0):
    trips = Trip.objects.all()[:5]
    months = Event.objects.filter(date__gt=now()).annotate(year_month=Concat(Year('date'), Month('date'))).\
        values('year_month').\
        annotate(total=Count('id'))
    months = map(map_months_counter, months)

    if year_month != 0:
        filter_date = datetime.strptime(year_month, '%Y-%m')
        events = Event.objects.filter(date__month=filter_date.month, date__year=filter_date.year)
    else:
        events = Event.objects.filter(date__gt=now())

    return render(request, 'website/travel.html', context={'trips': trips, 'events': events, 'months': months,
                                                           'year_month': year_month})


def view_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'website/trip.html', context={'trip': trip})


def view_event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'website/event.html', context={'event': event})


def travel_info(request):
    cats = Category.objects.all()
    return render(request, 'website/travel-ajax.html', context={'categories': cats})


def safety_insurance(request):
    return render(request, 'website/safety_insurance.html')


def request_quote(request):
    return render(request, 'website/request_quote.html')


def contact_us(request):
    data = request.POST.dict()
    if data:
        del data['csrfmiddlewaretoken']
        contact = ContactRequest.objects.create(**data)
        contact.save()
    return render(request, 'website/contact-us.html')


def testimonials(request):
    data = Testimonial.objects.all()

    return render(request, 'website/testimonials.html', context={"data": data})
