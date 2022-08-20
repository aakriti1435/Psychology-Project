from django.db import models
from accounts.constants import *
from django.utils.html import strip_tags
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Pages(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    content = RichTextUploadingField()
    type_id = models.PositiveIntegerField(choices=PAGE_TYPE)
    created_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        return data

    class Meta:
        managed = True
        db_table = 'tbl_page'