from django.db import models
from django.urls import reverse #Функция reverse позволяет генерировать URL-адреса динамически, используя именованные URL-шаблоны, что делает код более гибким и поддерживаемым при изменении маршрутов веб-приложения.
# Create your models here.

#основная модель веб-приложения в целом для реаллзиации основного функционала, а именно удаления фона
class Data(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')  # Поле для хранения имени пользователя
    image = models.ImageField(upload_to='users_images/%Y/%m/%d', blank=True)  # Поле для загрузки изображения пользователя
    archive = models.FileField(upload_to='user_archives/%Y/%m/%d/', blank=True)  # Поле для загрузки архива пользователя
    result_image = models.ImageField(upload_to='image_result/%Y/%m/%d', blank=True)  # Поле для сохранения обработанного изображения
    result_archive = models.FileField(upload_to='archive_result/%Y/%m/%d/', blank=True)  # Поле для сохранения обработанного архива
    bgcolor = models.CharField(max_length=15, verbose_name='Цвет фона', default=None, null=True)  # Поле для хранения цвета фона

    def __str__(self): #магический метод.переопределяет строковое представление объекта класса. Например в html шаблонах
        return str(self.pk)

    def get_absolute_url(self):
        return reverse()  # Возвращает URL для доступа к объекту модели

    class Meta:
        verbose_name = 'База пользовательских данных'  # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'База пользовательских данных'  # Человекочитаемое имя модели во множественном числе
        ordering = ['name',]  # Сортировка объектов модели по имени


