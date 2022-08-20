from .views import *
from django.conf.urls import url
from django.contrib import admin


admin.autodiscover()
app_name = 'services'


urlpatterns = [

    url(r'^$', ServicesList, name='services_list'),
    url(r'^add-service/$', AddService, name='add_service'),
    url(r'^delete-service/(?P<id>[-\w]+)/$', DeleteService, name='delete_service'),
    url(r'^view-service/(?P<id>[-\w]+)/$', ViewService, name='view_service'),
    url(r'^edit-service/(?P<id>[-\w]+)/$', EditService, name='edit_service'),
    
]
