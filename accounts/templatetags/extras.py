from accounts.models import *
from django import template
from page.models import Pages
from contact.models import ContactUs
from services.models import Services
from ratings.models import RatingReviews

register = template.Library()


@register.filter(name='total_pages')
def total_pages(key):
	return Pages.objects.all().count()


@register.filter(name='total_contacts')
def total_contacts(key):
	return ContactUs.objects.all().count()


@register.filter(name='total_services')
def total_services(key):
	return Services.objects.all().count()


@register.filter(name='total_ratings')
def total_ratings(key):
	return RatingReviews.objects.all().count()
