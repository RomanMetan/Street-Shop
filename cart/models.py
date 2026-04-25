from django.db import models

from django.db import models
from django.conf import settings
from catalog.models import Product
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="cart"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.user.username}"

    def get_total_price(self):
        """Общая стоимость всех товаров в корзине"""
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Товар в корзине"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name="Корзина",
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    added_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ('cart', 'product')  # Один товар в корзине может быть только один раз

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        """Стоимость позиции в корзине"""
        return self.product.price * self.quantity

    @receiver(post_save, sender=User)
    def create_user_cart(sender, instance, created, **kwargs):
        """Автоматически создаёт корзину при регистрации пользователя"""
        if created:
            Cart.objects.create(user=instance)