from django import forms
from .models import Birthday
# from .validators import real_age
from django.core.exceptions import ValidationError

# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


# class BirthdayForm(forms.Form):
#     first_name = forms.CharField(label='Имя', max_length=20)
#     last_name = forms.CharField(
#         label='Фамилия', required=False, help_text='Необязательное поле'
#     )
#     birthday = forms.DateField(
#         label='Дата рождения',
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         # В аргументе validators указываем список или кортеж
#         # валидаторов этого поля (валидаторов может быть несколько).
#         validators=(real_age,),
#     )
class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_first_name(self):  # Очищаем сложные имена до первого слова
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам
        # и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):
        # Вызов родительского метода clean.
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )
