from .models import *
from django import forms #Модуль forms предоставляет классы и функции для создания форм в Django.
from .models import Data #импорт моделей
from django.core.validators import FileExtensionValidator # для ограничения типов файлов, которые можно загружать в форму
import re #регулярные выражения для проверки валидности поля bgcolor
from cropbgsite.constants import regular_expression #импортируем наше регулярное выражение


# форма для класса представления СropOneView
class CropOneForm(forms.ModelForm):
    image = forms.ImageField(label='Загрузите изображение:') # то, что будет написано рядом с полем в форме, как пояснение
    bgcolor = forms.CharField(max_length=15, label='Цвет фона:', required=False) #настройка поля формы. required - обязательность поля. False - значит можно не заполнять. Заполнится указанным значением по умолчанию. Указано в модели

    #определение информации, которая будет указана в форме. Типо замена дефолтной формы по умолчанию которую предоставляет сам джанго. В дефолтной форме все поля модели есть.
    class Meta:
        model = Data
        fields = ['image', 'bgcolor'] # какие конкретно поля будут в форме
        error_messages = {
            'image': {'invalid_extension': "Пожалуйста, загрузите файлы только с расширениями 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'jfif', 'tiff', 'raw'"}
        } #текст сообщения, для ошибок и исключений которые мы определили ниже. Конкретно invalid_extension приввязан к allowed_extensions. Ошибка вызывается в шаблоне - {{ form.bgcolor.errors }}

    def __init__(self, *args, **kwargs): #магическая функция
        super().__init__(*args, **kwargs)
        self.fields['image'].validators.append(
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'jfif', 'tiff', 'raw'])
        )

    def clean_bgcolor(self): #проверка валидности поля bgcolor при его заполнении
        bgcolor = self.cleaned_data.get('bgcolor') # получаема то, что ввели в поле bgcolor

        # проверка есть ли что-то в поле bgcolor. То есть заполнил ли пользователь это поле
        if bgcolor:
            #если заполнил - проверяем на соответсвтие регулярному вырежению нашему. то есть присваивем переменной наше регулярное выражение чтобы применить метод match для проверки
            regex = regular_expression # переменная из cropbgsite.constants

            if not re.match(regex, bgcolor): #непосредственно сама проверка. если не соответсвует то вызываем ошибку forms.ValidationError

                raise forms.ValidationError('Некорректный формат цвета фона. Пожалуйста, введите в формате "R,G,B,A".')

        return bgcolor #возвращает то что пользователь заполнил с вызванной или не вызванной ошибкой? эту ошибку потом можно вызвать в html шаблоне {{ form.bgcolor.errors }}


# форма для класса представления CropArchiveForm
class CropArchiveForm(forms.ModelForm):
    archive = forms.FileField(label='Загрузите архив:') # то, что будет написано рядом с полем в форме, как пояснение
    bgcolor = forms.CharField(max_length=15, label='Цвет фона:', required=False) #настройка поля формы. required - обязательность поля. False - значит можно не заполнять. Заполнится указанным значением по умолчанию. Указано в модели

    class Meta:
        model = Data
        fields = ['archive',"bgcolor"] # какие конкретно поля будут в форме
        error_messages = {
            'archive': {'invalid_extension': 'Пожалуйста, загрузите файлы только с расширениями .zip или .rar.',}
        } #текст ошибки при рэйзе исключения из функции ниже см выше

    #позволяет загружать только rar и zip архивы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['archive'].validators.append(
            FileExtensionValidator(allowed_extensions=['zip', 'rar'])
        ) #смотри выше

    def clean_bgcolor(self): # смотри выше
        bgcolor = self.cleaned_data.get('bgcolor')
        if bgcolor:
            regex = regular_expression
            if not re.match(regex, bgcolor):
                raise forms.ValidationError('Некорректный формат цвета фона. Пожалуйста, введите в формате "R,G,B,A".')
        return bgcolor



