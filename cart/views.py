from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Robot

from .forms import OrderForm
from .models import Cart, CartItem, Order, OrderItem


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


@login_required
def checkout_view(request):
    """
    Оформление заказа: показывает форму с данными покупателя и сводку корзины,
    по POST создаёт Order + OrderItem'ы (снимок данных) и очищает корзину.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('robot').all()

    if cart.is_empty():
        messages.error(request, 'Добавьте товары в корзину.')
        return redirect('cart:index')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                comment=form.cleaned_data['comment'],
                total_price=cart.total_price(),
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    robot=item.robot,
                    robot_name=item.robot.name,
                    price=item.robot.price,
                    quantity=item.quantity,
                )
            items.delete()
            return redirect('cart:success', order_id=order.id)
    else:
        initial = {
            'first_name': request.user.first_name,
            'email': request.user.email,
        }
        form = OrderForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
        'items': items,
    }
    return render(request, 'cart/checkout.html', context)


@login_required
def order_success_view(request, order_id):
    """Страница подтверждения успешно оформленного заказа."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    items = order.items.all()

    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'cart/success.html', context)