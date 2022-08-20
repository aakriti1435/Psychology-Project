from django.db import models
from accounts.models import *


class ContactUs(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        managed = True;
        db_table = 'tbl_contact_us'


class ContactUsReply(models.Model):
    reply_message = models.TextField(null=True, blank=True)
    contact = models.ForeignKey(ContactUs, null=True, blank=True , on_delete=models.CASCADE)
    replied_by = models.ForeignKey(User, null=True, blank=True , on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        managed = True;
        db_table = 'tbl_contact_reply'
