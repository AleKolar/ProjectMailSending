from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create_newsletter/$', views.create_newsletter, name='create_newsletter'),
]