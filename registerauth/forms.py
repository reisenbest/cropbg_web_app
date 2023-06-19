from django.contrib.auth.forms import *
from django.contrib.auth.models import User

#немного адаптируем под нас стандартные дджанговские формы, добавляем стили, меняем label
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#немного адаптируем под нас стандартные дджанговские формы, добавляем стили, меняем label
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = User #используем стандарную модель джанго, поля из нее
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs): #немного магии
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'  # Дополнительный атрибут для пароля

    def get_form(self, *args, **kwargs): # и еще магия
        form = super().get_form(*args, **kwargs)
        form.fields['username'].widget.attrs['autocomplete'] = 'off'
        form.fields['password1'].widget.attrs['autocomplete'] = 'off'
        form.fields['password2'].widget.attrs['autocomplete'] = 'off'
        form.fields['password2'].widget.attrs['autocomplete'] = 'new-password'  # Дополнительный атрибут для пароля
        form.fields['password2'].widget.attrs.pop('autofill', None)  # Удаление атрибута autofill
        return form