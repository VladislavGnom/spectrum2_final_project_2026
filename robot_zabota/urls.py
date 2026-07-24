"""
Главный роутер проекта.

'/'          -> лендинг (core)
'/catalog/'  -> заготовка каталога роботов
'/cart/'     -> заготовка корзины
'/blog/'     -> заготовка блога с кейсами
'/profile/'  -> заготовка личного кабинета (users)
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('cart/', include('cart.urls')),
    path('blog/', include('blog.urls')),
    path('profile/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)