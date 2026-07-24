from django.db import models


class ContactRequest(models.Model):
    """Заявка, оставленная через форму обратной связи на лендинге."""
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Заявка с сайта'
        verbose_name_plural = 'Заявки с сайта'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.email})'