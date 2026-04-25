from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),  # 👈 ИСПОЛЬЗУЕМ CustomLogoutView
]