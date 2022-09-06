from django.db import models
from django.contrib.auth.models import AbstractUser
from user.token import Jwt


class User(AbstractUser):
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=20)
    is_verify = models.BooleanField(default=False)


    class Meta:
        db_table='user'



    @property
    def token(self):
        return Jwt.encode_token({'user_id': self.id,'username':self.username})
