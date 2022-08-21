from .views import *
from django.conf.urls import url
from django.contrib import admin


admin.autodiscover()
app_name = 'ratings'


urlpatterns = [
    url(r'^$', RatingReviewsList, name='ratings_list'),
    url(r'^rate-our-services/$', RateUsForm, name='rate_us'),
    url(r'^delete-review/(?P<id>[-\w]+)/$', DeleteReview, name='delete_review'),
    url(r'^view-review/(?P<id>[-\w]+)/$', ViewReview, name='view_review'),
]
