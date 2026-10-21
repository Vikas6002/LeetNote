# accounts/models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_lang  = models.CharField(max_length=30, default='python')
    total_solved    = models.IntegerField(default=0)
    streak          = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"