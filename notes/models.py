from django.db import models
from user.models import User


# Create your models here.
class Notes(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
