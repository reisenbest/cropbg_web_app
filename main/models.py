from django.db import models
from django.urls import reverse

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')  # Поле для хранения имени пользователя
    feedback = models.TextField(verbose_name='Напишите что-нибудь')  # Поле для хранения текста обратной связи
    time_upload = models.DateTimeField(auto_now_add=True)  # Поле для хранения времени загрузки обратной связи (автоматически заполняется при создании)

    class Meta:
        verbose_name = 'Обратная связь'  # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'Обратная связь'  # Человекочитаемое имя модели во множественном числе
        ordering = ['time_upload', 'name']  # Сортировка записей по времени загрузки и имени

    def __str__(self):
        return str(self.pk)  # Возвращает строковое представление первичного ключа объекта

    def get_absolute_url(self):
        return reverse()  # Возвращает URL-адрес объекта обратной связи (не указан конкретный URL-шаблон)
