import json

from django.db import models


class Robot(models.Model):
    """
    Модель робота-няни, представленного в каталоге.

    features хранится как JSON-строка (список характеристик),
    чтобы не создавать отдельную модель ради простого списка.
    Используйте get_features_list() для получения списка в шаблонах/коде.
    """
    name = models.CharField('Название модели', max_length=200)
    slug = models.SlugField('URL (slug)', unique=True)
    short_description = models.CharField('Короткое описание', max_length=300)
    full_description = models.TextField('Полное описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Фото', upload_to='robots/', blank=True)
    features = models.TextField(
        'Характеристики (JSON-список строк)',
        default='[]',
        help_text='Пример: ["Пульсоксиметр", "Видеосвязь 24/7", "Датчик падений"]',
    )
    is_available = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Робот'
        verbose_name_plural = 'Роботы'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_features_list(self):
        """Возвращает характеристики как список строк. При ошибке — пустой список."""
        try:
            data = json.loads(self.features)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, TypeError):
            pass
        return []