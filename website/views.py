from django.shortcuts import render


def index(request):
    return render(request, 'website/index.html')


def our_story(request):
    return render(request, 'website/our-story.html')


def travel(request):
    return render(request, 'website/travel.html')


def travel_info(request):
    from website.models import Category
    cats = Category.objects.all()
    return render(request, 'website/travel-ajax.html', context={'categories': cats})


def safety_insurance(request):
    return render(request, 'website/safety_insurance.html')


def request_quote(request):
    return render(request, 'website/request_quote.html')


def contact_us(request):
    return render(request, 'website/contact-us.html')


def testimonials(request):
    from website.models import Testimonial
    data = Testimonial.objects.all()

    return render(request, 'website/testimonials.html', context={"data": data})
