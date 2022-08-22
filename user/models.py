from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    location = models.CharField(max_length=20)

    def __str__(self):
        return str(self.first_name)
