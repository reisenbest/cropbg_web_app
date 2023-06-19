from django.conf.urls.static import static  # Импортируем функцию static для обработки статических файлов
from django.urls import include, path  # Импортируем функции include и path для определения URL-шаблонов
from cropbgsite import settings  # Импортируем настройки проекта
from .views import *  # Импортируем все представления из модуля views

urlpatterns = [
    path('cropimages/', cropimages, name='crop'),
    path('croponeimg/', СropOneView.as_view(), name='cropone'),
    path('croparchive/', CropArchiveView.as_view(), name='croparchive'),
    path('resultoneimg/<int:pk>/', ResultOneImg.as_view(), name='resultoneimg'),
    path('resultarchive/<int:pk>/', ResultArchiveView.as_view(), name='resultarchive'),
    path('finalimg/<int:pk>/', FinalImageView.as_view(), name='finalimg'),
    path('finalarchive/<int:pk>/', FinalArchiveView.as_view(), name='finalarchive'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #отвечает за добавление URL-шаблонов для обслуживания медиафайлов в режиме отладки (DEBUG=True).
# проще говоря, нужно чтобы чтобы в режиме отладки рабботал весь функционал. Например чтобы соххранить в бд загруженное пользователем изображение для него нужно создать папку
# Функция static() добавляет URL-шаблон для маршрутизации запросов к медиафайлам, определенным в настройках MEDIA_URL и MEDIA_ROOT.