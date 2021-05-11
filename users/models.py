from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        unique=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=30,
        unique=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=Role.choices,
        default=Role.USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True
    )

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    def get_payload(self):
        return {
            'user_id': self.id,
            'email': self.email,
            'username': self.username
        }

    class Meta:
        ordering = ('username', )
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
