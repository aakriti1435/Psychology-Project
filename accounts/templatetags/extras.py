from accounts.models import *
from django import template

from page.models import Pages

register = template.Library()


# @register.filter(name='total_users')
# def total_users(key):
# 	return User.objects.filter(role_id=USER).count()
