from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q



def product_list(request):
    """Список всех товаров"""
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    """Детальная страница товара"""
    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)


def product_list_by_category(request, category_slug):
    """Список товаров по категории"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, stock__gt=0)
    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'catalog/product_list.html', context)


def search_products(request):
    """Поиск товаров"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(stock__gt=0)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'results_count': products.count()
    }
    return render(request, 'catalog/search_results.html', context)