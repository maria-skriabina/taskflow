from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админ-панель для кастомного пользователя"""
    
    # Поля, которые отображаются в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Поля в форме редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'bio', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Поля при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone'),
        }),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('username',)
# Register your models here.
