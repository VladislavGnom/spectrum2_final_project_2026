from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.

    Поле username скрыто от пользователя и генерируется автоматически
    из локальной части email (до символа @), с проверкой на уникальность.
    """
    email = forms.EmailField(
        label='Email',
        required=True,
        error_messages={
            'required': 'Пожалуйста, укажите email.',
            'invalid': 'Введите корректный email-адрес.',
        },
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
    )
    first_name = forms.CharField(
        label='Имя',
        required=True,
        max_length=150,
        error_messages={'required': 'Пожалуйста, укажите имя.'},
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].error_messages['required'] = 'Пожалуйста, введите пароль.'
        self.fields['password2'].error_messages['required'] = 'Пожалуйста, подтвердите пароль.'
        self.fields['password1'].help_text = 'Минимум 8 символов, не должен быть слишком простым.'
        self.fields['password2'].help_text = 'Введите тот же пароль ещё раз для подтверждения.'
        # Поле username не показываем пользователю — генерируется автоматически.
        if 'username' in self.fields:
            del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def _generate_username(self, email):
        base = email.split('@')[0] or 'user'
        username = base
        counter = 1
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f'{base}{counter}'
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.username = self._generate_username(user.email)
        if commit:
            user.save()
        return user