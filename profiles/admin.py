from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Встраиваем профиль в страницу пользователя"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'


class CustomUserAdmin(UserAdmin):
    """Расширенная админка пользователя"""
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'phone', 'delivery_address', 'created_at']  # 👈 ИСПРАВЛЕНО
    list_filter = ['gender', 'created_at']  # 👈 ИСПРАВЛЕНО
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']  # 👈 ИСПРАВЛЕНО

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Личная информация', {
            'fields': ('age', 'gender', 'phone')
        }),
        ('Доставка', {
            'fields': ('delivery_address',)
        }),
        ('Аватар', {
            'fields': ('avatar',)
        }),
        ('Системное', {
            'fields': ('created_at',)  # 👈 ИСПРАВЛЕНО
        }),
    )


# Перерегистрируем модель User с нашей админкой
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)