from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, UserInfoForm
from cart.models import Cart


@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    user = request.user
    profile = user.profile

    # Получаем корзину пользователя
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.items.all()
    cart_total = cart.get_total_price()

    # Получаем заказы пользователя (сортировка от новых к старым)
    orders = user.orders.all().order_by('-created_at')

    if request.method == 'POST':
        user_form = UserInfoForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Профиль успешно обновлён!')
            return redirect('profiles:profile')
        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме')
    else:
        user_form = UserInfoForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'orders': orders,  # 👈 ЗАКАЗЫ ПЕРЕДАЮТСЯ В ШАБЛОН
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def profile_orders(request):
    """История заказов пользователя (отдельная страница, если нужна)"""
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'profiles/orders.html', {'orders': orders})