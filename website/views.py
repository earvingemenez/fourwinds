from django.shortcuts import render


def index(request):
    return render(request, 'website/index.html')


def our_story(request):
    return render(request, 'website/our-story.html')


def travel(request):
    return render(request, 'website/travel.html')


def safety_insurance(request):
    return render(request, 'website/safety_insurance.html')


def request_quote(request):
    return render(request, 'website/request_quote.html')


def contact_us(request):
    return render(request, 'website/contact-us.html')
