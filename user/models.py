from django.db import models
from django.contrib.auth.models import AbstractUser


#  Custom User Manager
class User(AbstractUser):

    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=20)

