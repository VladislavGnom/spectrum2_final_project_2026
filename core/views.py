import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import ContactForm


def index(request):
    """Одностраничный лендинг: Hero, О проекте, Команда, Контакты."""
    return render(request, 'core/index.html')


@require_http_methods(['POST'])
def contact_submit(request):
    """
    Приём формы обратной связи через fetch (без перезагрузки страницы).

    Ожидает JSON {name, email, message}. Сейчас только валидирует и
    возвращает статус — интеграцию с почтой/CRM подключить здесь позже.
    """
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        payload = request.POST

    form = ContactForm(payload)
    if form.is_valid():
        # ЗАМЕНИТЬ: здесь в будущем — отправка письма или сохранение лида.
        return JsonResponse({'ok': True, 'message': 'Мы подберём решение для вашей семьи и свяжемся с вами в ближайшее время'})

    return JsonResponse({'ok': False, 'errors': form.errors.get_json_data()}, status=400)
