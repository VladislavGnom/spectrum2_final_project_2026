from django import forms


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