from django.db import models

class Users(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    age = models.IntegerField(null=True)
    mail_address = models.EmailField()
    delete_flag = models.BooleanField(default=False)
    created_add = models.DateTimeField(auto_now_add=True)
    updated_add = models.DateTimeField(auto_now=True)