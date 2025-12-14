from django.db import models
from django.contrib.auth.models import User
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
    
    creator = models.ForeignKey(
        User,
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
    
    def str(self):
        return self.title
    
    def is_overdue(self):
        """Проверка, просрочена ли задача"""
        if self.deadline and self.status != self.Status.COMPLETED:
            return timezone.now() > self.deadline
        return False
