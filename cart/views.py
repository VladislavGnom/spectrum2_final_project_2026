from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Robot

from .models import Cart, CartItem


@login_required
def cart_view(request):
    """Показывает содержимое корзины текущего пользователя."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('robot').all()

    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'cart/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, robot_id):
    """Добавляет робота в корзину. Если он уже там — увеличивает количество."""
    robot = Robot.objects.filter(pk=robot_id, is_available=True).first()

    if robot is None:
        messages.error(request, 'Этот робот сейчас недоступен для заказа.')
        return redirect('catalog:index')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, robot=robot)
    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f'«{robot.name}» добавлен в корзину.')
    return redirect('cart:index')


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Обновляет количество товара в корзине (или удаляет при quantity < 1)."""
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        item.delete()
        messages.success(request, 'Товар удалён из корзины.')
    else:
        item.quantity = quantity
        item.save()

    return redirect('cart:index')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Удаляет товар из корзины."""
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Товар удалён из корзины.')
    return redirect('cart:index')