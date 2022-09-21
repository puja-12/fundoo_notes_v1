from django.db import models

from labels.models import Labels
from user.models import User


# Create your models here.
class Notes(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1200)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    labels = models.ManyToManyField(Labels)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-id']

    def __str__(self):
        return self.title
