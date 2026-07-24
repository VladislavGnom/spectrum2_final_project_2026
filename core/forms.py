from django import forms


class ContactForm(forms.Form):
    """
    Форма обратной связи в секции «Контакты».

    Сейчас используется только для валидации на бэкенде (на случай, если
    фронтенд-валидация будет обойдена). Отправка писем / сохранение в БД —
    добавить позже, когда появится реальный канал связи.
    """
    name = forms.CharField(
        label='Имя',
        max_length=100,
        error_messages={'required': 'Пожалуйста, укажите ваше имя.'},
    )
    email = forms.EmailField(
        label='Email',
        error_messages={
            'required': 'Пожалуйста, укажите email.',
            'invalid': 'Проверьте корректность email.',
        },
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea,
        error_messages={'required': 'Пожалуйста, добавьте сообщение.'},
    )
