from django.shortcuts import render


def index(request):
    return render(request, 'website/index.html')


def safety_insurance(request):
    return render(request, 'website/safety_insurance.html')
