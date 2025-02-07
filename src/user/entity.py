from lc.entity import BaseEntity
from django.db import models

class User(BaseEntity):
    id = models.BigIntegerField(blank=False, primary_key=True)
    username = models.CharField(blank=False, max_length=80)
    password = models.CharField(blank=False, max_length=200)
    email = models.CharField(blank=False, max_length=100)