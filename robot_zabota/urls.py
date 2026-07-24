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

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('cart/', include('cart.urls')),
    path('blog/', include('blog.urls')),
    path('profile/', include('users.urls')),
]
