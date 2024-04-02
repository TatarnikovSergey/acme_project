from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .validators import real_age


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    # price = models.IntegerField(
    #     validators=(MaxValueValidator(100), MinValueValidator(10)))
    image = models.ImageField('Фото', blank=True, upload_to='birthday_images')

    class Meta:
        # Проверка уникальных значений всех полей в совокупности
        constraints = (models.UniqueConstraint(
            fields=('first_name', 'last_name', 'birthday'),
            name='Unique person constraint',
            ),
        )
        verbose_name = 'человек'
