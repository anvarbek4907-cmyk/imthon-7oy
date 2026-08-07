from django.db import models
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(
        max_length=255
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    image = models.ImageField(
        upload_to='posts/'
    )

    desc = models.TextField(
        max_length=300
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    body = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.author.username} - {self.post.title}"