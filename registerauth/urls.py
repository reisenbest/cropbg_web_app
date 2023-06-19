from django.conf.urls.static import static
from django.urls import  path
from cropbgsite import settings
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),#обработчик странички регистрации. Использует класс представления
    path('login/', LoginUser.as_view(), name='login'),#обработчик странички с обратной авторизации. Использует класс представления
    path('logout/', CustomLogoutView.as_view(), name='logout'),#обработчик странички разлогинивания. Использует класс представления

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#отвечает за добавление URL-шаблонов для обслуживания медиафайлов в режиме отладки (DEBUG=True).
# проще говоря, нужно чтобы чтобы в режиме отладки рабботал весь функционал. Например чтобы соххранить в бд загруженное пользователем изображение для него нужно создать папку
# Функция static() добавляет URL-шаблон для маршрутизации запросов к медиафайлам, определенным в настройках MEDIA_URL и MEDIA_ROOT.