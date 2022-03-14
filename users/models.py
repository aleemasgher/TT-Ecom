from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.FloatField(default=1000)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
