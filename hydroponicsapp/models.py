from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser, User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import json

#Registration (Create Account)
class Registration (AbstractUser):
    
    date_created = models.DateField(auto_now_add=True, null=True, verbose_name='date created')

class Notifications (Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Read','Read'),
    )  

    ALERT = (
        ('High', 'High'),
        ('Low', 'Low'),
    )

    date_time = models.DateTimeField(auto_now_add = True)
    sensor = models.CharField(max_length = 200)
    measurement = models.CharField(max_length = 200)
    alert = models.CharField(max_length=10, choices=ALERT)
    status = models.CharField(max_length=10, choices=STATUS)