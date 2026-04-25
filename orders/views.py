from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm, FakePaymentForm


@login_required
def checkout(request):
    """Оформление заказа"""
    cart = Cart.objects.get(user=request.user)

    if cart.items.count() == 0:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session['checkout_data'] = {
                'delivery_address': form.cleaned_data['delivery_address'],
                'payment_method': form.cleaned_data['payment_method'],
                'total_amount': str(cart.get_total_price()),
            }
            return redirect('orders:payment')
    else:
        initial = {}
        if request.user.profile.delivery_address:
            initial['delivery_address'] = request.user.profile.delivery_address
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def fake_payment(request):
    """Страница фейк-оплаты (принимает любую карту)"""
    checkout_data = request.session.get('checkout_data')

    if not checkout_data:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = FakePaymentForm(request.POST)
        if form.is_valid():
            # Принимаем любую карту (без проверки)
            cart = Cart.objects.get(user=request.user)

            # Создаём заказ
            order = Order.objects.create(
                user=request.user,
                delivery_address=checkout_data['delivery_address'],
                total_amount=checkout_data['total_amount'],
                payment_method=checkout_data['payment_method'],
                status='paid'  # Оплачен
            )

            # Переносим товары из корзины в заказ
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.price,
                    quantity=cart_item.quantity
                )

            # Очищаем корзину
            cart.items.all().delete()

            # Очищаем сессию
            del request.session['checkout_data']

            # Сохраняем ID заказа для страницы успеха
            request.session['paid_order_id'] = order.id

            messages.success(request, f'✅ Заказ #{order.id} успешно оплачен!')
            return redirect('orders:payment_success')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля корректно')
    else:
        form = FakePaymentForm()

    context = {
        'form': form,
        'total_amount': checkout_data['total_amount'],
    }
    return render(request, 'orders/fake_payment.html', context)


@login_required
def payment_success(request):
    """Страница успешной оплаты"""
    order_id = request.session.get('paid_order_id')
    if not order_id:
        return redirect('catalog:product_list')

    order = get_object_or_404(Order, id=order_id, user=request.user)
    del request.session['paid_order_id']

    return render(request, 'orders/payment_success.html', {'order': order})