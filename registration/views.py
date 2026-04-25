from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import RegistrationForm


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'{user.first_name}, добро пожаловать в Street Shop!')
            return redirect('catalog:product_list')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Кастомное представление входа"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:product_list')


class CustomLogoutView(LogoutView):
    """Представление выхода - перенаправляет на главную"""
    next_page = '/'  # 👈 ГЛАВНОЕ - перенаправление на главную