from django.shortcuts import render


def index(request):
    """
    Заготовка личного кабинета.

    ЗАМЕНИТЬ: когда подключится авторизация (или расширение auth.User),
    добавить сюда историю заказов, профиль и настройки пользователя.
    """
    context = {
        'placeholder_title': 'Личный кабинет',
        'placeholder_text': 'Скоро здесь будет личный кабинет',
    }
    return render(request, 'users/stub.html', context)
