from django.db import models
from django.contrib.auth.models import AbstractUser
from core.enums.user import UserRoles


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=UserRoles.choices())

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
