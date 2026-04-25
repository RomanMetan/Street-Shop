from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('registration.urls')),
    path('profile/', include('profiles.urls')),  # если создали
    path('', include('catalog.urls')),           # ГЛАВНАЯ СТРАНИЦА (каталог)
    path('cart/', include('cart.urls')),  # 👈 ДОБАВИТЬ
    path('orders/', include('orders.urls')),  # 👈 ДОБАВЬТЕ ЭТУ СТРОЧКУ

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

