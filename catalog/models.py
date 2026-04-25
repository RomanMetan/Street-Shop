from django.db import models


class Category(models.Model):
    """Категория товара"""
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""
    name = models.CharField("Название товара", max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Количество на складе", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        """Возвращает True, если товар есть в наличии"""
        return self.stock > 0