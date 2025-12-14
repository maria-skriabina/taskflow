from django.contrib import admin
from .models import Task, UserProfile

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tasks_created_count', 'tasks_completed_count']
    search_fields = ['user__username']
