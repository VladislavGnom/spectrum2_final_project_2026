from django import template

register = template.Library()


@register.filter(name='ru_pluralize')
def ru_pluralize(value, forms):
    """
    Корректное склонение существительных после числительных для русского языка.

    Использование в шаблоне:
        {{ count|ru_pluralize:"товар,товара,товаров" }}

    forms — строка из трёх форм через запятую: единственное число (1, 21, 31...),
    родительный падеж единственного числа (2-4, 22-24...) и родительный падеж
    множественного числа (5-20, 25-30...).

    Если value не приводится к int или forms заданы не в виде трёх частей —
    возвращает пустую строку, чтобы ошибка в шаблоне не приводила к 500-й ошибке.
    """
    try:
        n = abs(int(value))
    except (TypeError, ValueError):
        return ''

    parts = forms.split(',')
    if len(parts) != 3:
        return ''
    one, few, many = (part.strip() for part in parts)

    if n % 10 == 1 and n % 100 != 11:
        return one
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return few
    return many