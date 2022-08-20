from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import *


"""
User Model
"""
class User(AbstractUser):
    username = models.CharField(max_length=150,blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=150,null=True,blank=True)
    first_name = models.CharField(max_length=150,null=True,blank=True)
    last_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField("email address", null=True, blank=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    role_id = models.PositiveIntegerField(default=1,choices=USER_ROLE, null=True, blank=True)
    state = models.PositiveIntegerField(default=1, choices=USER_STATUS, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        managed = True;
        db_table = 'tbl_user'

    def __str__(self):
        return str(self.username)


"""
Login History
"""
class LoginHistory(models.Model):
    user_ip = models.CharField( max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(default=timezone.now, max_length=255, null=True, blank=True)
    code = models.CharField(default=timezone.now, max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.CharField( max_length=255, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_login_history'
