import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


# Домены временных/одноразовых почтовых сервисов.
# ПОПОЛНИТЬ при необходимости — список не исчерпывающий.
DISPOSABLE_EMAIL_DOMAINS = {
    'mailinator.com',
    'tempmail.com',
    '10minutemail.com',
    'guerrillamail.com',
    'throwawaymail.com',
    'yopmail.com',
    'temp-mail.org',
}


class OrderForm(forms.Form):
    """Форма оформления заказа."""
    first_name = forms.CharField(
        label='Имя',
        max_length=150,
        error_messages={'required': 'Пожалуйста, укажите имя.'},
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
    )
    email = forms.EmailField(
        label='Email',
        error_messages={
            'required': 'Пожалуйста, укажите email.',
            'invalid': 'Введите корректный email.',
        },
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        error_messages={'required': 'Пожалуйста, укажите телефон.'},
        widget=forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67'}),
    )
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Город, улица, дом, квартира'}),
        error_messages={'required': 'Пожалуйста, укажите адрес.'},
    )
    comment = forms.CharField(
        label='Комментарий к заказу',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Дополнительная информация...'}),
    )

    def clean_phone(self):
        """
        Приводит телефон к единому формату +7XXXXXXXXXX.

        Принимает российские номера, начинающиеся с +7 или 8
        и содержащие ровно 11 цифр (например: +7 (999) 123-45-67,
        89991234567, +79991234567).
        """
        raw = self.cleaned_data.get('phone', '')

        # Оставляем только цифры и ведущий "+", остальное (скобки, дефисы,
        # пробелы) отбрасываем.
        cleaned = re.sub(r'(?!^\+)[^\d]', '', raw.strip())
        digits = re.sub(r'\D', '', cleaned)

        error = ValidationError(
            'Введите корректный номер телефона (например, +7 999 123-45-67)'
        )

        if len(digits) != 11:
            raise error

        if digits.startswith('8'):
            digits = '7' + digits[1:]
        elif not digits.startswith('7'):
            raise error

        return f'+{digits}'

    def clean_email(self):
        """
        Нормализует email (нижний регистр, без пробелов по краям),
        проверяет его валидность и отклоняет одноразовые почтовые домены.
        """
        email = self.cleaned_data.get('email', '').strip().lower()

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Введите корректный email.')

        domain = email.rsplit('@', 1)[-1]
        if domain in DISPOSABLE_EMAIL_DOMAINS:
            raise ValidationError(
                'Пожалуйста, укажите постоянный email. Временные адреса не принимаются.'
            )

        return email