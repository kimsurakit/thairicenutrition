from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    institute = models.CharField(max_length=50)
