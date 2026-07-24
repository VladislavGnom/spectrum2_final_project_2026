from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Robot


def catalog_view(request):
    """
    Список роботов в каталоге.

    Обычным посетителям показываются доступные модели (is_available=True)
    и модели «скоро в продаже» (coming_soon=True). Администраторам
    (is_staff) — вообще все модели, включая полностью скрытые, чтобы
    можно было проверить карточку до публикации.
    """
    if request.user.is_authenticated and request.user.is_staff:
        robots = Robot.objects.all()
    else:
        robots = Robot.objects.filter(Q(is_available=True) | Q(coming_soon=True))

    context = {
        'robots': robots,
        'page_title': 'Каталог CAREBOTS',
    }
    return render(request, 'catalog/catalog.html', context)


def robot_detail_view(request, slug):
    """Детальная страница одного робота."""
    robot = get_object_or_404(Robot, slug=slug)
    context = {
        'robot': robot,
        'features_list': robot.get_features_list(),
    }
    return render(request, 'catalog/robot_detail.html', context)