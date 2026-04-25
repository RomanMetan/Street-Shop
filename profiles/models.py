from django.db import models
from django.contrib.auth.models import User

class Gender(models.TextChoices):
    MALE = 'M', 'Мужской'
    FEMALE = 'F', 'Женский'

class UserProfile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="profile"
    )

    # Только дополнительные поля (которых нет в User)
    age = models.PositiveIntegerField("Возраст", null=True, blank=True)
    gender = models.CharField("Пол", max_length=1, choices=Gender.choices, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    delivery_address = models.TextField("Адрес доставки", blank=True)
    avatar = models.ImageField("Аватар", upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профиль {self.user.username}"

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email


# Сигналы для автоматического создания профиля
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создаёт профиль при создании нового пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    # Проверяем, существует ли профиль, чтобы избежать ошибки
    if hasattr(instance, 'profile'):
        instance.profile.save()