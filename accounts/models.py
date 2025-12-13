from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Наследуемся от стандартной AbstractUser и добавляем свои поля.
    """
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='Аватар',
        blank=True,
        null=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        null=True,
        max_length=500
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
