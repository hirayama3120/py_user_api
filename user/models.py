from django.db import models

class Users(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    age = models.IntegerField(null=True)
    mail_address = models.EmailField()
    created_add = models.DateTimeField(auto_now_add=True)
    update_add = models.DateTimeField(auto_now=True)