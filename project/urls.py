"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
# from . import views


urlpatterns = [
   path('admin/', admin.site.urls),
    # path('subscribe/', views.subscribe_view, name='subscribe'),
   path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом products/.
   # path('posts/', include('news.urls')),
   path('news/', include('news.urls_news')),
    # path('articles/', include('news.urls_articles')), ######## НОВОЕ
    # path('subscribe/', include('news.urls_subscribe')),
   # path('', include('news.urls')), # пока убрал чтобы не конфликтовало, не знаю правильный вариант

    # ДОБАВКИ
    path('', include('protect.urls')), # пока убрал чтобы не конфликтовало, не знаю правильный вариант
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),

    # ПОЧТА
    # path('appointments/', include('appointments.urls')), #этот вариант здесь не работает - непонятно почему!
    path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),

    # path('articles/', ArtList.as_view(), name='art_list'),
]


# Добавляем обслуживание медиафайлов в режиме разработки
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

