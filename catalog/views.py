from django.shortcuts import render


def index(request):
    """
    Заготовка страницы каталога.

    ЗАМЕНИТЬ: когда появятся модели товаров (Robot, Category и т.д.),
    подключить сюда список моделей роботов, фильтры и карточки товаров.
    """
    context = {
        'placeholder_title': 'Каталог роботов',
        'placeholder_text': 'Скоро здесь будет каталог',
    }
    return render(request, 'catalog/stub.html', context)
