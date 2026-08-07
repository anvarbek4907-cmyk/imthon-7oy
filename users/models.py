from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    first_name = models.CharField(
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        max_length=150,
        blank=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png'
    )

    bio = models.TextField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    social_links = models.JSONField(
        default=dict,
        blank=True
    )

    def __str__(self):
        return self.username