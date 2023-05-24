from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self",
        related_name="following",
        symmetrical=False,
        blank=True,
    )

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    def follow(self, user):
        if not self.is_following(user):
            self.followers.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followers.remove(user)

    def is_following(self, user):
        return self.followers.filter(id=user.id).exists()



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
