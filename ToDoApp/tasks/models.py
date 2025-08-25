from django.db import models
from users.models import User

# Create your models here.    

class Task(models.Model):
    
    title = models.CharField(max_length=45, null=False)
    description = models.CharField(max_length=200, null=False)
    status = models.CharField(max_length=10, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()