import re
from datetime import date, datetime
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import Concat
from website.models import Trip, Event, Category, Testimonial, Month, Year, ContactRequest, Quote

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.conf import settings


def index(request):
    return render(request, 'website/index.html')


def our_story(request):
    return render(request, 'website/our-story.html')


def category_travels(request, category_id):
    category = Category.objects.get(id=category_id)
    trips = []
    events = []
    for sub in category.subcategories:
        trips = trips + [t for t in sub.trips if t not in trips]
        events = events + [e for e in sub.events if e not in events]
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
    category = trip.subcategories.all()[0].category
    return render(request, 'website/trip.html', context={'trip': trip, 'category': category})


def view_event(request, event_id):
    event = Event.objects.get(id=event_id)
    category = event.subcategories.all()[0].category
    return render(request, 'website/event.html', context={'event': event, 'category': category})


def travel_info(request):
    cats = Category.objects.all().order_by('rank')
    subcats = []
    for c in cats:
        subcats = subcats + [s for s in c.subcategories]
    return render(request, 'website/travel-ajax.html', context={'categories': cats, 'subcategories': subcats})


def safety_insurance(request):
    return render(request, 'website/safety_insurance.html')


def request_quote(request, details=''):
    if not details:
        data = request.POST.dict()
        if data:
            del data['csrfmiddlewaretoken']
            data['meal_to_include'] = ", ".join(request.POST.getlist('meal'))
            quote = Quote.objects.get(id=int(data['id']))
            quote.followup_time = data.get('followup_time')
            quote.chaperones = int(0 if not data.get('chaperones') else data.get('chaperones'))
            quote.department = data.get('department')
            quote.transportation = data.get('transportation')
            quote.preferred_airport = data.get('preferred_airport')
            quote.meal_to_include = data.get('meal_to_include')
            if request.FILES.get('attachment'):
                quote.attachment = request.FILES.get('attachment')
            quote.save()
            kwargs=model_to_dict(quote)
            send_email('quote', **kwargs)
            send_email('thank-you', to_email=contact.email, **kwargs)
        return render(request, 'website/request_quote.html')
    else:
        data = request.POST.dict()
        data['date'] = '{}-{}-{}'.format(data['date[year]'], data['date[month]'], data['date[day]'])
        del data['csrfmiddlewaretoken']
        del data['date[year]'], data['date[month]'], data['date[day]']
        quote = Quote.objects.create(**data)
        quote.save()
        return render(request, 'website/request_quote_details.html', context={"quote_id": quote.id})


def contact_us(request):
    data = request.POST.dict()
    if data:
        del data['csrfmiddlewaretoken']
        contact = ContactRequest.objects.create(**data)
        contact.save()
        kwargs = model_to_dict(contact)
        send_email('contact-us', **kwargs)
        send_email('thank-you', to_email=contact.email, **kwargs)

    return render(request, 'website/contact-us.html')


def testimonials(request):
    data = Testimonial.objects.all()
    return render(request, 'website/testimonials.html', context={"data": data})


def send_email(template, from_email='noreply@fourwindstours.com', to_email='accounts@fourwindstours.com', **kwargs):
    to_email = to_email if to_email else kwargs.get('email')
    # to_email = 'amielsinue@gmail.com'
    if not to_email:
        return
    msg_plain = render_to_string('website/emails/{}.txt'.format(template), {"data": kwargs.items()})
    msg_html = render_to_string('website/emails/{}.html'.format(template), {"data": kwargs.items()})
    try:
        send_mail('Conact Us', msg_plain, from_email=from_email, recipient_list=[to_email],
                  fail_silently=False, html_message=msg_html)
    except Exception as e:
        error = e
        pass