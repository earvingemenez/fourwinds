from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^safety_and_insurance/$', views.safety_insurance, name='safety_insurance'),
]
