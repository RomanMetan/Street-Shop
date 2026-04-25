from django.db import models

from django.db import models
from django.conf import settings
from catalog.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', '🟡 Новый'),
        ('paid', '🟢 Оплачен'),
        ('processing', '📦 В обработке'),
        ('shipped', '🚚 Отправлен'),
        ('delivered', '✅ Доставлен'),
        ('cancelled', '❌ Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    related_name="orders"  # 👈 ЭТО ВАЖНО

    )

    created_at = models.DateTimeField("Дата заказа", auto_now_add=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')

    # Адрес доставки (копия на момент заказа)
    delivery_address = models.TextField("Адрес доставки")

    # Итоговая сумма
    total_amount = models.DecimalField("Итоговая сумма", max_digits=10, decimal_places=2)

    # Данные для фейк-оплаты
    payment_method = models.CharField("Способ оплаты", max_length=50, default='card')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    """Товар в заказе (снимок на момент покупки)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    product_name = models.CharField("Название товара", max_length=200)
    product_price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество")

    def get_total_price(self):
        return self.product_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"