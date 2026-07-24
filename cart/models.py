from django.conf import settings
from django.db import models

from catalog.models import Robot


class Cart(models.Model):
    """
    Корзина пользователя. Один пользователь — одна корзина,
    создаётся автоматически при первом добавлении товара (get_or_create во view).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {self.user}'

    def total_price(self):
        return sum((item.subtotal() for item in self.items.all()), 0)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def is_empty(self):
        return not self.items.exists()


class CartItem(models.Model):
    """Позиция в корзине: конкретный робот и его количество."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE, verbose_name='Робот')
    quantity = models.PositiveIntegerField('Количество', default=1)
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.robot.name} × {self.quantity}'

    def subtotal(self):
        return self.robot.price * self.quantity