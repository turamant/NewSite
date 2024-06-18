from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email

