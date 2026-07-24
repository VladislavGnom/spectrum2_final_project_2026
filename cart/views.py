from django.shortcuts import render


def index(request):
    """
    Заготовка страницы корзины.

    ЗАМЕНИТЬ: когда появится модель Order/CartItem, подключить сюда
    состав корзины, расчёт суммы и переход к оформлению заказа.
    """
    context = {
        'placeholder_title': 'Корзина',
        'placeholder_text': 'Скоро здесь будет корзина',
    }
    return render(request, 'cart/stub.html', context)
