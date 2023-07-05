from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth import get_user_model

# User = get_user_model()

class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True)
    first_name = models.TextField("Имя", max_length=150)
    last_name = models.TextField("Фамилия", max_length=150)
    email = models.EmailField(
        "Электронная почта", unique=True, blank=False, max_length=254
    )

    USERNAME_FIELD = "username"
    UNIQUE_FIELDS = ["username",'email']
    REQUIRED_FIELDS = ["email", "first_name", "last_name","password"]
