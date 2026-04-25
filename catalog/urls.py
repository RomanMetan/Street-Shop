# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('catalog/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('search/', views.search_products, name='search'),  # 👈 ДОБАВИТЬ

]