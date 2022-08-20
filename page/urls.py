from .views import *
from django.conf.urls import url
from django.contrib import admin


admin.autodiscover()
app_name = 'page'


urlpatterns = [
    url(r'^add-page/$', AddPage, name='add_page'),
    url(r'^pages/$', PagesView, name='page_list'),
    url(r'^delete-page/$', DeletePage, name='delete_page'),
    url(r'^view-page/(?P<id>[-\w]+)/$', ViewPage, name='view_page'),
    url(r'^edit-page/(?P<id>[-\w]+)/$', PageEdit, name='edit_page'),
    url(r'^change-state/(?P<id>[-\w]+)/$', ChangeState, name='change_state'),
]
