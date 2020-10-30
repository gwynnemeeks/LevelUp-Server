"""Gamer model module"""
from django.db import models
from django.contrib.auth.models import User


class Gamer(models.Model):
    """Gamer database model"""
    bio = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)