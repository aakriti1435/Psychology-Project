from .views import *
from django.conf.urls import url
from django.contrib import admin


admin.autodiscover()
app_name = 'contact'


urlpatterns = [
    url(r'^$', ContactsList, name='contacts_list'),
    url(r'^contacts-graph$', ContactsGraph, name='contacts_graph'),
    url(r'^contact-us/$', ContactFormView, name='contact_form'),
    url(r'^delete-contact/(?P<id>[-\w]+)/$', DeleteContact, name='delete_contact'),
    url(r'^view-contact/(?P<id>[-\w]+)/$', ViewContact, name='view_contact'),
]


