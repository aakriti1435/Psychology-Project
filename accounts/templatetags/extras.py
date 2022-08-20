'''
/**
 *@copyright : ToXSL Technologies Pvt. Ltd. < www.toxsl.com >
 *@author     : Shiv Charan Panjeta < shiv@toxsl.com >
 *
 * All Rights Reserved.
 * Proprietary and confidential :  All information contained herein is, and remains
 * the property of ToXSL Technologies Pvt. Ltd. and its partners.
 * Unauthorized copying of this file, via any medium is strictly prohibited.
 **/
'''

from accounts.models import *
from django import template

from page.models import Pages

register = template.Library()


# @register.filter(name='total_users')
# def total_users(key):
# 	return User.objects.filter(role_id=USER).count()
