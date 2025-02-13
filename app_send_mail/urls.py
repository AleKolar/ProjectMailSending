from django.conf.urls import url

from app_send_mail import views

urlpatterns = [url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^newsletter/$', views.create_newsletter, name='newsletter'),

]


