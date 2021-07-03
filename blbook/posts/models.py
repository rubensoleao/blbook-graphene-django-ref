from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    text = models.CharField(max_length=100)
    posted_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    posted_at = models.DateField(default=datetime.now())

    def __str__(self):
        return "{self.text}"
