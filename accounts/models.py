from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=150, unique=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='followings')
