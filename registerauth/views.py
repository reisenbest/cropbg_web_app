from django.shortcuts import render
from cropbgsite.constants import menu, log_sign
from django.contrib.auth.forms import *
from django.contrib.auth.views import *
from django.views.generic import *
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import login

# Create your views here.

#отвечает за регистрацию пользователя
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registerauth/register.html'

    def form_valid(self, form):
        # сохраняем то что пользователь ввел в форму в переменную
        response = super().form_valid(form)

        # Автоматическая авторизация пользователя. Чтобы когда пользователь зарегистрировался ему не пришлось логинится, а он сразу был авторизован
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)

        return response

    # перенаправление в случае успешного заполнения формы (авторизация\регистрация\выход)
    def get_success_url(self):
        return reverse_lazy('home')

    #описание в других views. crop.views, main.views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['log_sign'] = log_sign
        return context

#Почти сам все делает благодаря LoginView+LoginUserForm
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registerauth/login.html'

    #перенаправление в случае успешного заполнения формы (авторизация\регистрация\выход)
    def get_success_url(self):
        return reverse_lazy('home')

    #получаем контекст. описание можно посмотреть в коде других приложений (crop, main)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['log_sign'] = log_sign
        return context


#разлогинивание осуществляет сам благодаря LogoutView. Просто говорим куда перенаправиться
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')