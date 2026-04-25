from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from catalog.models import Product
from .models import Cart, CartItem
from .forms import AddToCartForm


@login_required
def cart_detail(request):
    """Просмотр корзины"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
def add_to_cart(request, product_slug):
    """Добавление товара в корзину с проверкой остатка"""
    product = get_object_or_404(Product, slug=product_slug)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Получаем текущий товар в корзине (если есть)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        # Текущее количество в корзине
        current_quantity = cart_item.quantity if cart_item else 0

        # Сколько всего будет после добавления
        total_quantity = current_quantity + quantity

        # Проверка: не превышает ли наличие на складе
        if total_quantity > product.stock:
            messages.error(request,
                           f'Нельзя добавить больше {product.stock} шт. товара "{product.name}". В наличии только {product.stock} шт.')
            return redirect('cart:cart_detail')

        # Если товар уже есть в корзине
        if cart_item:
            cart_item.quantity = total_quantity
            cart_item.save()
            messages.success(request, f'Количество товара "{product.name}" обновлено до {total_quantity} шт.')
        else:
            # Создаём новый товар в корзине
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            messages.success(request, f'Товар "{product.name}" добавлен в корзину в количестве {quantity} шт.')

        return redirect('cart:cart_detail')

    return redirect('catalog:product_detail', slug=product_slug)


@login_required
def update_cart_item(request, item_id):
    """Обновление количества товара в корзине с проверкой остатка"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Проверка: не превышает ли наличие на складе
        if quantity > cart_item.product.stock:
            messages.error(request,
                           f'Нельзя установить больше {cart_item.product.stock} шт. В наличии только {cart_item.product.stock} шт.')
        elif quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Количество товара "{cart_item.product.name}" обновлено до {quantity} шт.')
        else:
            cart_item.delete()
            messages.success(request, f'Товар "{cart_item.product.name}" удалён из корзины')

        return redirect('cart:cart_detail')


@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Товар "{product_name}" удалён из корзины')
    return redirect('cart:cart_detail')