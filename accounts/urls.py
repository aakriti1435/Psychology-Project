from django.conf.urls import url
from django.contrib import admin
from .views import *

admin.autodiscover()

app_name = 'accounts'

urlpatterns = [

    ## Index Graph and Authentication
    url(r'^user-graph/$', UserGraph, name='user_graph'),
    url(r'^revenue-graph/$', RevenueGraph, name='revenue_graph'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),

    ## User
    url(r'^delete-user/$', DeleteUser, name='delete_user'),
    url(r'^edit-user/(?P<id>[-\w]+)/$', EditUser, name='edit_user'),
    url(r'^users/$', Allusers, name='allusers'),
    url(r'^view/(?P<id>[-\w]+)/$',ViewUser, name='view_user'),

    ## Validations
    url(r'^change-password/$', PasswordChange.as_view(), name='Password_Change'),

    ## Login History
    url(r'^login-history/$', LoginHistoryView, name='login_history'),
    url(r'^delete-history/$', DeleteHistory, name='delete_history'),


]