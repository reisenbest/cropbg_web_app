from django.conf.urls.static import static
from django.urls import path
from cropbgsite import settings
from .views import *

urlpatterns = [
    path('', mainpage, name='home'),
    path('about/', about, name='about'),
    path('userguide/', userguide, name='userguide'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'), #обработчик странички с обратной связью. Использует класс представления
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#отвечает за добавление URL-шаблонов для обслуживания медиафайлов в режиме отладки (DEBUG=True).
# проще говоря, нужно чтобы чтобы в режиме отладки рабботал весь функционал. Например чтобы соххранить в бд загруженное пользователем изображение для него нужно создать папку
# Функция static() добавляет URL-шаблон для маршрутизации запросов к медиафайлам, определенным в настройках MEDIA_URL и MEDIA_ROOT.