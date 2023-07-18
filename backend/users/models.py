from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        "имя пользователя", max_length=150, unique=True
    )
    first_name = models.TextField("Имя", max_length=150)
    last_name = models.TextField("Фамилия", max_length=150)
    email = models.EmailField(
        "Электронная почта", unique=True, blank=False, max_length=254
    )

    USERNAME_FIELD = "username"
    UNIQUE_FIELDS = ["username", "email"]
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "password"]

    class Meta:
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="кто подписан",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="на кого подписан",
    )

    class Meta:
        unique_together = ["user", "following"]
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"Пользователь {self.user} подписан на {self.following}"
