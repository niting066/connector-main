from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid

User = get_user_model()


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', default='def_image.jpg')
    location = models.CharField(max_length=100, blank=True, default='None')

    def __str__(self):
        return self.user.username


class UserPosting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='timeline')
    caption = models.TextField()
    uploaded_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user


class FollowAccount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
