from django.db import models
from django.core import validators
# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(blank=False ,null=False)
    number = models.CharField(max_length=13,null=True, blank=False)
    message = models.TextField()
    is_seen = models.BooleanField(default=False, null=False, blank=False)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        db_table = 'contacts'

    def __str__(self):
        return self.name
