from accounts.models import *
from django import template
from page.models import Pages
from contact.models import ContactUs

register = template.Library()


@register.filter(name='total_pages')
def total_pages(key):
	return Pages.objects.all().count()


@register.filter(name='total_contacts')
def total_contacts(key):
	return ContactUs.objects.all().count()
