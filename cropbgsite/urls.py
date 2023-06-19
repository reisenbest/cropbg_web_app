"""
URL configuration for cropbgsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from cropbgsite import settings



urlpatterns = [
    path('admin/', admin.site.urls), #админ-панель
    # включения URL-шаблонов из приложения с именем main.urls. Это означает, что при обращении к корневому адресу <адрес вашего приложения>/, запросы будут обрабатываться с помощью URL-шаблонов, определенных в main.urls.
    path('', include('main.urls')),

    # включения URL-шаблонов из приложения с именем register.urls. Это означает, что при обращении к корневому адресу <адрес вашего приложения>/, запросы будут обрабатываться с помощью URL-шаблонов, определенных в registerauth.urls.
    path('', include('registerauth.urls')),

    # включения URL-шаблонов из приложения с именем crop.urls. Это означает, что при обращении к корневому адресу <адрес вашего приложения>/, запросы будут обрабатываться с помощью URL-шаблонов, определенных в crop.urls.
    path('', include('crop.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#отвечает за добавление URL-шаблонов для обслуживания медиафайлов в режиме отладки (DEBUG=True).
# проще говоря, нужно чтобы чтобы в режиме отладки рабботал весь функционал. Например чтобы соххранить в бд загруженное пользователем изображение для него нужно создать папку
# Функция static() добавляет URL-шаблон для маршрутизации запросов к медиафайлам, определенным в настройках MEDIA_URL и MEDIA_ROOT.