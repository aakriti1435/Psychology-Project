from .views import *
from django.conf.urls import url
from django.contrib import admin


admin.autodiscover()
app_name = 'services'


urlpatterns = [
    url(r'^$', ServicesList, name='services_list'),
    # url(r'^contact-us/$', ContactFormView, name='contact_form'),
    # url(r'^delete-contact/(?P<id>[-\w]+)/$', DeleteContact, name='delete_contact'),
    # url(r'^view-contact/(?P<id>[-\w]+)/$', ViewContact, name='view_contact'),
]
