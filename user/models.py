from django.db import models
from django.contrib.auth.models import AbstractUser


#  Custom User Manager
from user.token import Jwt


class User(AbstractUser):

    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=20)
    is_verify = models.BooleanField(default=False)

    @property
    def token(self):
        return Jwt.encode({'user_id':self.id})