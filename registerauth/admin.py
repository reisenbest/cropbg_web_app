from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('id',) + UserAdmin.list_display  #берем из стандартнйор модели поля для отображения и добавляем 'id' к списку отображаемых столбцов

# Зарегистрируйте модель User с новым классом Admin

#убираем стандартную модель джанго и свою регистрируем, она представляет собой стандартную+включает дополнения которые мы выше описали. (одно поле другое)_
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)