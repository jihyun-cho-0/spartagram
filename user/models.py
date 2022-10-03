# user/models.py
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"
        

    author_name = models.CharField(max_length=10, default='')
    bio = models.CharField(max_length=100, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    updated_at = models.DateTimeField(auto_now=True)


