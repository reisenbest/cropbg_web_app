from .models import *
from django import forms

#форма для обработки класса представления, реализующего оставление отзывов пользователями
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback #модель указали
        fields = ['feedback',] #отображаемые поля
