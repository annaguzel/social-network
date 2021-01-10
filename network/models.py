import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=500)
    user = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now=timezone.now())
    likes = models.ManyToManyField(
        User, related_name='post_like', null=True, blank=True)

    def number_of_likes(self):
        return self.likes.count()
