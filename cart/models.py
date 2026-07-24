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


class Order(models.Model):
    """Заказ, созданный из корзины."""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь',
    )
    first_name = models.CharField('Имя', max_length=150)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес доставки')
    comment = models.TextField('Комментарий к заказу', blank=True)
    total_price = models.DecimalField('Сумма заказа', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ №{self.id} — {self.user}'


class OrderItem(models.Model):
    """Товар в заказе (снимок данных на момент покупки)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    robot = models.ForeignKey('catalog.Robot', on_delete=models.SET_NULL, null=True, verbose_name='Робот')
    robot_name = models.CharField('Название робота', max_length=200)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f'{self.robot_name} × {self.quantity}'

    def subtotal(self):
        return self.price * self.quantity