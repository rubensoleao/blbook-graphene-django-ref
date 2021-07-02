from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    text = models.CharField(max_length=100)
    posted_by = models.ForeignKey(        
        User, related_name="posts", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text

