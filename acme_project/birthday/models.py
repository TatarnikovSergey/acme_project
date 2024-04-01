from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField('Дата рождения')
    # price = models.IntegerField(
    #     validators=(MaxValueValidator(100), MinValueValidator(10)))
