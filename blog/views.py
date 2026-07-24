from django.http import Http404
from django.shortcuts import render

from .cases import CASES


def blog_view(request):
    """Список историй семей (кейсов), которым помог робот-няня."""
    context = {
        'cases': CASES,
        'page_title': 'Истории заботы',
    }
    return render(request, 'blog/blog.html', context)


def case_detail_view(request, case_id):
    """Детальная страница одной истории."""
    case = next((c for c in CASES if c['id'] == case_id), None)
    if case is None:
        raise Http404('История не найдена')

    context = {
        'case': case,
        'page_title': case['title'],
    }
    return render(request, 'blog/case_detail.html', context)