from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="following"
    )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")
