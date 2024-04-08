from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .validators import real_age
from django.urls import reverse
from django.contrib.auth import get_user_model

# Да, именно так всегда и ссылаемся на модель пользователя!
User = get_user_model()


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    # price = models.IntegerField(
    #     validators=(MaxValueValidator(100), MinValueValidator(10)))
    image = models.ImageField('Фото', blank=True, upload_to='birthday_images')
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})

    class Meta:
        # Проверка уникальных значений всех полей в совокупности
        constraints = (models.UniqueConstraint(
            fields=('first_name', 'last_name', 'birthday'),
            name='Unique person constraint',
            ),
        )
        verbose_name = 'человек'
        verbose_name_plural = 'люди'


