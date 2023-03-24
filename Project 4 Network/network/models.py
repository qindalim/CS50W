from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=1000, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, blank=True, related_name="all_likes")

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, blank=True, related_name="all_following")
    follower = models.ManyToManyField(User, blank=True, related_name="all_follower")
    