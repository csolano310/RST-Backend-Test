from django.db import models

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=45, null=False)
    email = models.EmailField(max_length=45, unique=True, null=False)
    password_hash = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField()
    token = models.CharField(max_length=100)