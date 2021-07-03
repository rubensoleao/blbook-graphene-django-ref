from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    user_followed = models.ForeignKey(
        User, related_name="followed_by", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Follow: {self.user} -> {self.user_followed}"
