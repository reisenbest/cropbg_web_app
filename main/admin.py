from django.contrib import admin
from .models import *
# Register your models here.

#регистрация модели в админ-панели, отвечает за сохранение отзывов пользователей в базе данных
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_upload', 'feedback') #какие поля модели будут отображаться в админ-модели
    list_editable = ('feedback',) #поля, которые можно редактировать
    list_filter = ('id', 'name', 'time_upload' ) #по каким полям модели можно фильтровать
    # search_fields -  список полей модели, по которым можно выполнять поиск записей в административной панели. Например: search_fields = ('name', 'id').
    # list_per_page - количество записей, отображаемых на одной странице в списке записей. Например: list_per_page = 20.
    # ordering - порядок сортировки записей. Например "ordering = ('-name')- сортирвка в обратном порядке
    # readonly_fields - список полей модели, доступных только для чтения в админ-панели readonly_fields = ('id',)
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options - подробнее

admin.site.register(Feedback, FeedbackAdmin) # обязательная команда для регистрации