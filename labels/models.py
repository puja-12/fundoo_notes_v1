from django.db import models
from user.models import User


class Labels(models.Model):
    label = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




