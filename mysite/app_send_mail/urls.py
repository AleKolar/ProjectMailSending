from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_newsletter/$', views.create_newsletter, name='create_newsletter'),
]