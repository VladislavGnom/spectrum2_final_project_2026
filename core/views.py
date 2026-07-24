import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import ContactRequest


def index(request):
    """Одностраничный лендинг: Hero, О проекте, Команда, Контакты."""
    return render(request, 'core/index.html')

@require_POST
def contact_submit(request):
    """
    Принимает данные формы обратной связи как JSON, валидирует их
    и сохраняет как заявку (ContactRequest) для последующей обработки в админке.
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'ok': False, 'errors': {'__all__': ['Некорректный формат запроса.']}}, status=400)

    form = ContactForm(data)

    if form.is_valid():
        ContactRequest.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            message=form.cleaned_data['message'],
        )
        return JsonResponse({
            'ok': True,
            'message': 'Спасибо! Мы свяжемся с вами в ближайшее время.',
        })

    return JsonResponse({
        'ok': False,
        'errors': form.errors,
    }, status=400)
