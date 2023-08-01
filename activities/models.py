from django.db import models

from users.models import User


class Activity(models.Model):
    created_by = models.ForeignKey(User, related_name='activities', on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    unit = models.CharField(max_length=50)
    carbon_footprint = models.FloatField()
    activity_type = models.IntegerField()
