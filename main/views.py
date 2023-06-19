from django.shortcuts import render
from django.http import HttpResponse
from cropbgsite.constants import menu, log_sign
from django.views.generic import CreateView
from .models import *
from .forms import *
from django.urls import reverse_lazy


# Create your views here.

'''При получении запроса, функция cropimages использует функцию render для формирования HTTP-ответа с помощью указанного 
'шаблона html. В этом случае, в контексте шаблона также передается переменная menu, которая содержит 
соответствующие данные меню.

Функция render берет запрос request, указывает шаблон html и передает словарь контекста, 
содержащий переменную menu. Контекст словаря позволяет передать данные из представления в шаблон, 
чтобы они могли быть использованы при рендеринге HTML-страницы.

В итоге, эта функция обрабатывает запросы к маршруту cropimages/ и возвращает ответ, 
включающий HTML-страницу, сформированную на основе указанного шаблона html и переданных данных контекста.''' #пояснение длинное
def mainpage(request):
    return render(request, 'main/main.html', {'menu': menu, 'log_sign': log_sign})


def about(request):
    return render(request, 'main/about.html', {'menu': menu, 'log_sign': log_sign})

def userguide(request):
    return render(request, 'main/userguide.html', {'menu': menu, 'log_sign': log_sign})



class FeedbackCreateView(CreateView):
    '''
    класс представленя для обаботки формы обратной связи
    '''
    template_name = 'main/feedback.html'
    model = Feedback
    form_class = FeedbackForm

    def form_valid(self, form):
        # Заполняем поле 'name' значением имени авторизованного пользователя
        form.instance.name = self.request.user.username

        #Вызывается метод form_valid базового класса представления, чтобы выполнить стандартную обработку формы. Он сохраняет форму, создает новый объект
        return super().form_valid(form)

    #перенаправление в случае успешного заполнения формы (авторизация\регистрация\выход)
    def get_success_url(self):
        return reverse_lazy('home')

    '''
    Метод get_context_data() используется для получения контекстных данных,
    которые будут переданы в шаблон при рендеринге представления. 
    В данном случае, метод расширяет базовую реализацию get_context_data() 
    путем вызова super().get_context_data(**kwargs), чтобы получить исходный контекст данных.
    '''  # пояснение длинное
    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs)  # с помощью super наследуем все что есть в родительской функции get_context_data
        context['menu'] = menu  # добавляем свои к уже имеющимя отродителя  get_context_data(**kwargs)
        context['log_sign'] = log_sign  # добавляем свои к уже имеющимя отродителя  get_context_data(**kwargs)
        return context  # возвращаем контекст в класс представления

