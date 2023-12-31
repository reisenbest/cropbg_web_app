from django.views.generic import CreateView, DetailView #импортируем необходимые классы представлений
from django.shortcuts import render
from django.http import HttpResponse
from cropbgsite.constants import * #наши постоянные переменные, тут и функции обработки изображений, и глобальные перменные
from .models import Data #модель нашу берем
from .forms import * #все формы из файла forms
from django.urls import reverse
from django.core.files.base import ContentFile
from cropbgsite.tasks import delete_data_from_DB # для удаления данных из БД через интервалы
from django.utils.encoding import smart_str # для скачивания архива. формирует имя
import os
import mimetypes # для скачивания архива. опеределяет тип
# Create your views here.



'''При получении запроса, функция cropimages использует функцию render для формирования HTTP-ответа с помощью указанного 
'шаблона crop/cropimages.html. В этом случае, в контексте шаблона также передается переменная menu, которая содержит 
соответствующие данные меню.

Функция render берет запрос request, указывает шаблон crop/cropimages.html и передает словарь контекста, 
содержащий переменную menu. Контекст словаря позволяет передать данные из представления в шаблон, 
чтобы они могли быть использованы при рендеринге HTML-страницы.

В итоге, эта функция обрабатывает запросы к маршруту cropimages/ и возвращает ответ, 
включающий HTML-страницу, сформированную на основе указанного шаблона crop/cropimages.html и переданных данных контекста.''' #пояснение длинное
def cropimages(request):
    return render(request, 'crop/cropimages.html', {'menu': menu})

def cropone(request):
    return render(request, 'crop/croponeimg.html', {'menu': menu})


#класс представления, отвечающий за удаление фона у одного изображеия.
class СropOneView(CreateView):
    template_name = 'crop/croponeimg.html' #передаем шаблон где все должно отображаться
    model = Data # передаем модель с которой будем работать
    form_class = CropOneForm #передаем нашу измененную под наши нужду форму. Ее мы создали и определили в файле forms.py

    #главная функция, отвечающая за весь функционал. Загрузку изображения и цвета фона в форму, ее обработку
    #начнет выполняться когда мы нажмем кнопку submit
    def form_valid(self, form):
        #Автоматически заполняем поле 'name' значением имени авторизованного сейчас пользователя, который и проводит операцию данную. Нужно чтобы в админ-панели мы видели какой пользователь загрузил эту форму
        form.instance.name = self.request.user.username

        # В данном коде используется метод save объекта формы для сохранения данных формы в базу данных. Однако, параметр commit=False указывает, что сохранение должно быть отложено и не выполняться непосредственно после вызова save. Другими словами запоминает данные и ждет пока я вызову data.save()
        data = form.save(commit=False)

        # image_file = form.cleaned_data['image'] переменная нигде не используется, но операция частая. очтавил пояснение. #берем изображение, которое пользователь загрузил в форму, очищаем его. Нужно для дальнейшей работы

        # промежуточное сохранние данных в форму. Нужно чтобы функция обработчика изображения, которое берет изображение и удаляет фон. Знала данные вроде рк или самого изображения c которым он будет работать
        data.save()

        # кладем в переменную то, что пользователь ввел в поле bgcolor. данные уже прошли валидацию в файле forms.py
        bg_color_one_img = data.bgcolor

        #кладем в переменную путь к изображению, которое пользоваьтель загрузил в форму
        image_path = data.image.path

        #наша функция-обработчк изображения. именно она удаляет фон. принимает путь к изображению, загруженному пользователь и к цвету фона если указал.Возвращает изображение в байтовом формате
        result_image = cropbg_one_img(image_path,bg_color_one_img)

        #имя загруженного пользовтелем изображения без расширения
        output_image_name = os.path.splitext(os.path.basename(data.image.name))[0]

        # Создаем объект ContentFile из байтов изображения
        result_image_content = ContentFile(result_image, name=(output_image_name+'.png'))

        # Сохраняем изображение в поле result_image модели data
        data.result_image.save((output_image_name+'.png'), result_image_content)
        data.save()

        '''
        В данном коде super().form_valid(form) вызывает метод form_valid() родительского класса (базового класса), 
        от которого наследуется текущий класс.
        
        Вызов super().form_valid(form) гарантирует выполнение базовой логики обработки формы, которую предоставляет родительский класс.
         Это может включать сохранение данных формы, выполнение дополнительных действий или перенаправление на другую страницу.

        Таким образом, данный код позволяет передать управление базовому классу для выполнения его логики обработки формы
         после проверки валидности.
        ''' #пояснение длинное
        return super().form_valid(form)

    #перенаправление в случае успешного заполнения формы (авторизация\регистрация\выход\успешная загрузка и обработка файлов формы)
    def get_success_url(self):
        #перенаправляет на шаблон resultoneimg + берет рк объекта, с которым мы работали в конкретном случае. объекта в БД. это передается и url в том числе
        return reverse('resultoneimg', kwargs={'pk': self.object.pk})

    '''
    Метод get_context_data() используется для получения контекстных данных,
     которые будут переданы в шаблон при рендеринге представления. 
     В данном случае, метод расширяет базовую реализацию get_context_data() 
     путем вызова super().get_context_data(**kwargs), чтобы получить исходный контекст данных.
     ''' #пояснение длинное
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #с помощью super наследуем все что есть в родительской функции get_context_data
        context['menu'] = menu #добавляем свои к уже имеющимя отродителя  get_context_data(**kwargs)
        context['log_sign'] = log_sign #добавляем свои к уже имеющимя отродителя  get_context_data(**kwargs)
        return context #возвращаем контекст в класс представления

'''
класс представления промежуточный, который по сути только и делает, 
что перенаправляет пользователя на скачивание файла. 
так как нет динамического обновления страницы - авточматическим перенаправлением 
пользователя на эту страницу мы говорим ему что все готово и можно скачивать
''' #длинное пояснение
class ResultOneImg(DetailView):
    template_name = 'crop/resultoneimg.html'
    model = Data

    # перенаправление на скачивание файла
    def get_success_url(self):
        return reverse('finalimg', kwargs={'pk': self.object.pk})

    #смотри выше
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['log_sign'] = log_sign
        # Получение объекта модели Data
        data = self.get_object()
        # Передача объекта модели Data в контекст шаблона
        context['data'] = data
        return context


#класс представления, отвечающий за удаление фона у архива изображений изображеия.
class CropArchiveView(CreateView):
    template_name = 'crop/croparchive.html' #передаем шаблон где все должно отображаться
    model = Data # передаем модель с которой будем работать# передаем модель с которой будем работать
    form_class = CropArchiveForm #передаем нашу измененную под наши нужду форму. Ее мы создали и определили в файле forms.py

    # главная функция, отвечающая за весь функционал. Загрузку изображения и цвета фона в форму, ее обработку
    # начнет выполняться когда мы нажмем кнопку submit
    def form_valid(self, form):
        # Автоматически заполняем поле 'name' значением имени авторизованного сейчас пользователя, который и проводит операцию данную. Нужно чтобы в админ-панели мы видели какой пользователь загрузил эту форму
        form.instance.name = self.request.user.username

        # В данном коде используется метод save объекта формы для сохранения данных формы в базу данных. Однако, параметр commit=False указывает, что сохранение должно быть отложено и не выполняться непосредственно после вызова save. Другими словами запоминает данные и ждет пока я вызову data.save()
        data = form.save(commit=False)

        # archive_file = form.cleaned_data['archive'] см в CropOneView

        # промежуточное сохранние данных в форму. Нужно чтобы функция обработчика изображения, которое берет изображение и удаляет фон. Знала данные вроде рк или самого изображения c которым он будет работать
        data.save()

        # кладем в переменную то, что пользователь ввел в поле bgcolor. данные уже прошли валидацию в файле forms.py
        bg_color_archive = data.bgcolor

        # кладем в переменную путь к архиву который пользоваьтель загрузил в форму
        archive_path = data.archive.path

        #сохраняем индивидуальный идентификатор для формирования уникальных имен для временных папок, которые создает функция по обработке архива
        pk = data.pk

        #основная функция, принимает путь к архиву, который пользователь загрузил и цвет фона. по умолчанию None возвращает архив как файл в байтовом формате? уточнить.
        result_archive_file = cropbg_archive(archive_path, data.pk, bg_color_archive)

        #формирует контент-файл с которым джанго работает и чтобы он был доступен для скачивания. Принимает то что вернула функция + имя нового файла который получится
        result_archive_content= ContentFile(result_archive_file, name=('result_archive' + str(data.pk) + '.zip'))

        #сохраняем в бд. указываем имя которое будет в бд + сам файл
        data.result_archive.save(('result_archive' + str(data.pk) + '.zip'), result_archive_content)
        data.save()

        #при обработке архива, в отличие от обработки одиночного изображения, создаются временные папки. Вот тут они удаляются
        delete_files_in_user_files()

        '''
        В данном коде super().form_valid(form) вызывает метод form_valid() родительского класса (базового класса), 
        от которого наследуется текущий класс.

        Вызов super().form_valid(form) гарантирует выполнение базовой логики обработки формы, которую предоставляет родительский класс.
        Это может включать сохранение данных формы, выполнение дополнительных действий или перенаправление на другую страницу.

        Таким образом, данный код позволяет передать управление базовому классу для выполнения его логики обработки формы
        после проверки валидности.
        '''  # пояснение длинное
        return super().form_valid(form)

    #перенаправление в случае успешного заполнения формы (авторизация\регистрация\выход\успешная загрузка и обработка файлов формы)
    def get_success_url(self):
        # перенаправляет на шаблон resultoneimg + берет рк объекта, с которым мы работали в конкретном случае. объекта в БД. это передается и url в том числе
        return reverse('resultarchive', kwargs={'pk': self.object.pk})

    '''
    Метод get_context_data() используется для получения контекстных данных,
     которые будут переданы в шаблон при рендеринге представления. 
     В данном случае, метод расширяет базовую реализацию get_context_data() 
     путем вызова super().get_context_data(**kwargs), чтобы получить исходный контекст данных.
     ''' #пояснение длинное
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #с помощью super наследуем все что есть в родительской функции get_context_data
        context['menu'] = menu #добавляем свои к уже имеющимя отродителя  get_context_data(**kwargs)
        context['log_sign'] = log_sign  #добавляем свои к уже имеющимя отродителя  get_context_data(**kwargs)
        return context #возвращаем контекст в класс представления

'''
класс представления промежуточный, который по сути только и делает, 
что перенаправляет пользователя на скачивание файла. 
так как нет динамического обновления страницы - авточматическим перенаправлением 
пользователя на эту страницу мы говорим ему что все готово и можно скачивать
''' #длинное пояснение
class ResultArchiveView(DetailView):
    template_name = 'crop/resultarchive.html'
    model = Data

    # перенаправление на скачивание файла
    def get_success_url(self):
        return reverse('finalimg', kwargs={'pk': self.object.pk})
    #смотри выше
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['log_sign'] = log_sign
        # Получение объекта модели Data
        data = self.get_object()
        # Передача объекта модели Data в контекст шаблона
        context['data'] = data
        return context

#отвечает за возможность скачаивания обработанных файлов. Для одиночного изображения
class FinalImageView(DetailView):
    # шаблон нужен только чтобы при нажатии кнопки скачать приложение брало файл и скачивало. шаблон испльзуется просто для перенаправления. Уверен можно умнее реализовать, но пока костыль.
    template_name = 'crop/finalimg.html'
    model = Data

    #основной функционал, который как раз и занимается тем, что делает файл из формы доступным для скачивания
    def get(self, request, *args, **kwargs):
        # нужно, чтобы функция понимала какой именно объект (с каким pk) нужно брать. мы этот pk передавали и в прошлом классе Result
        instance = self.get_object()

        #формируем имя изображения, которое скачает пользователь. добавляем к имени загруженного изображения формат пнг и все. а так имся такое же должно быть
        output_image_name = os.path.splitext(os.path.basename(instance.result_image.name))[0]+'.png'

        #берем изображение из базы данных
        image_data = instance.result_image.read()

        #формируем респонс http. говорим что хотим отдать и указываем тип файла.
        response = HttpResponse(image_data, content_type="image/png")

        # позволяет указать браузеру, что ответ должен быть вложенным файлом и задает имя файла.
        response['Content-Disposition'] = f'attachment; filename="{output_image_name}"'


        '''
        Возвращаем объект response из представления. 
        Когда браузер получает этот ответ, он будет предложен 
        сохранить изображение с указанным именем как файл для загрузки.
        ''' #длинное пояснение
        return response

#отвечает за возможность скачаивания обработанных файлов. Для архива
class FinalArchiveView(DetailView):
    # шаблон нужен только чтобы при нажатии кнопки скачать приложение брало файл и скачивало. шаблон испльзуется просто для перенаправления. Уверен можно умнее реализовать, но пока костыль.
    template_name = 'crop/finalarchive.html'
    model = Data

    def get(self, request, *args, **kwargs):
        # Получаем объект Data, связанный с представлением Нужно, чтобы функция понимала какой именно объект (с каким pk) нужно брать. мы этот pk передавали и в прошлом классе Result
        instance = self.get_object()

        # Получаем путь к файлу в поле result_archive
        file_path = instance.result_archive.path

        # Открываем файл в режиме чтения бинарного файла
        with open(file_path, 'rb') as f:
            # Читаем содержимое файла
            file_data = f.read()

        # Определяем тип содержимого файла на основе его расширения
        content_type, encoding = mimetypes.guess_type(file_path)

        # Если тип содержимого не определен, устанавливаем значение по умолчанию
        content_type = content_type or 'application/octet-stream'

        # Создаем объект HttpResponse с содержимым файла и типом содержимого
        response = HttpResponse(file_data, content_type=content_type)

        # Устанавливаем заголовок Content-Disposition, чтобы браузер скачал файл с исходным именем
        response['Content-Disposition'] = f'attachment; filename="{smart_str(instance.result_archive.name)}"'

        # Возвращаем HttpResponse объект в качестве ответа на запрос
        return response


delete_data_from_DB() #периодческое очищенние базы данных. ЧТобы ээкономить место