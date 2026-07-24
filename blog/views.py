from django.shortcuts import render


def index(request):
    """
    Заготовка страницы блога.

    ЗАМЕНИТЬ: когда появится модель Post, подключить сюда список статей
    и кейсов внедрения с превью, тегами и датами публикации.
    """
    context = {
        'placeholder_title': 'Блог с кейсами',
        'placeholder_text': 'Скоро здесь будет блог',
    }
    return render(request, 'blog/stub.html', context)
