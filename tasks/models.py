from django.db import models
from django.conf import settings  # Импортируем settings
from django.utils import timezone

class Task(models.Model):
    """
    Модель задачи (Task)
    """
    # Константы для выбора
    class Status(models.TextChoices):
        NEW = 'NEW', 'Новая'
        IN_PROGRESS = 'IN_PROGRESS', 'В процессе'
        COMPLETED = 'COMPLETED', 'Выполнена'
    
    class Priority(models.IntegerChoices):
        LOW = 1, 'Низкий'
        MEDIUM = 2, 'Средний'
        HIGH = 3, 'Высокий'
    
    # Поля модели
    title = models.CharField(
        max_length=200,
        verbose_name='Название задачи'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    #Используем settings.AUTH_USER_MODEL
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Создатель'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус'
    )
    
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name='Приоритет'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Срок выполнения'
    )
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """Проверка, просрочена ли задача"""
        if self.deadline and self.status != self.Status.COMPLETED:
            return timezone.now() > self.deadline
        return False


class UserProfile(models.Model):
    """
    Расширенный профиль пользователя
    """
    # ИСПРАВЛЕНО: Используем settings.AUTH_USER_MODEL
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ← ВОТ ТАК!
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    
    tasks_created_count = models.IntegerField(
        default=0,
        verbose_name='Создано задач'
    )
    
    tasks_completed_count = models.IntegerField(
        default=0,
        verbose_name='Выполнено задач'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания профиля'
    )
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    def update_stats(self):
        """Обновление статистики пользователя"""
        self.tasks_created_count = self.user.created_tasks.count()
        self.tasks_completed_count = self.user.created_tasks.filter(
            status=Task.Status.COMPLETED
        ).count()
        self.save()


# Сигналы для автоматического создания профиля
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Создать профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Сохранить профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)
