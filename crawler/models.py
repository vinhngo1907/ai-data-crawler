from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random, math

class KeyWord(models.Model):
    """
    Keywords Table
    """

    name = models.CharField()

class Category(models.Model):
    def save(self, *args, **kwargs):
        print("Save Function")