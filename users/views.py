from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm


def register_view(request):
    """
    Регистрация нового пользователя с автоматическим входом
    сразу после успешной отправки формы.
    """
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


class UserLoginView(LoginView):
    """Стандартный вход по email (USERNAME_FIELD модели User)."""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный email или пароль.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = 'core:index'


login_view = UserLoginView.as_view()
logout_view = UserLogoutView.as_view()


@login_required
def profile_view(request):
    """
    Личный кабинет пользователя. Пока показывает заглушку под историю
    заказов — расширить, когда появится интеграция с cart/catalog.
    """
    return render(request, 'users/profile.html')