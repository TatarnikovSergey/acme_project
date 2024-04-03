# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


# Создаём миксин.
class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayCreateView(BirthdayMixin, CreateView):
    form_class = BirthdayForm
    pass


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    form_class = BirthdayForm
    pass


# class BirthdayCreateView(CreateView):
#     """Создание объектов модели."""
#     # Указываем модель, с которой работает CBV...
#     model = Birthday
#     # # Этот класс сам может создать форму на основе модели!
#     # # Нет необходимости отдельно создавать форму через ModelForm.
#     # # Указываем поля, которые должны быть в форме:
#     # fields = '__all__'
#     # А можно использовать уже созданную форму с уже настроенными проверками:
#     form_class = BirthdayForm
#     # Явным образом указываем шаблон (если не указывать то имя
#     # шаблона должно быть "имя-модели_form.html" типа birthday_form.html):
#     template_name = 'birthday/birthday_form.html'
#     # Указываем namespace:name страницы, куда будет перенаправлен пользователь
#     # после создания объекта:
#     success_url = reverse_lazy('birthday:list')
#
#
# class BirthdayUpdateView(UpdateView):
#     model = Birthday
#     form_class = BirthdayForm
#     template_name = 'birthday/birthday_form.html'
#     success_url = reverse_lazy('birthday:list')


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    """Класс для отображения списка объектов."""
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    """Удаление объекта"""
    # Атрибуты наследуются от BirthdayMixin
    pass


# class BirthdayDeleteView(DeleteView):
#     """Удаление объекта"""
#     model = Birthday
#     # template_name = 'birthday/birthday_form.html' # Создали другой шаблон удаления
#     success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday
    # Переопределяем или дополняем словарь контекста:
    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context


# # Добавим опциональный параметр pk для выбора редактируемого объекта.
# def birthday(request, pk=None):  # А это уже форма для POST запросов
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
#     if pk is not None:
#         # Получаем объект модели или выбрасываем 404 ошибку.
#         instance = get_object_or_404(Birthday, pk=pk)
#     # Если в запросе не указан pk
#     # (если получен запрос к странице создания записи):
#     else:
#         # Связывать форму с объектом не нужно, установим значение None.
#         instance = None
#     # Передаём в форму либо данные из запроса, либо None.
#     # В случае редактирования прикрепляем объект модели.
#     form = BirthdayForm(
#         request.POST or None,
#         # Файлы, переданные в запросе, указываются отдельно.
#         files=request.FILES or None,
#         instance=instance)
#     # Остальной код без изменений.
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday_form.html', context)


# def birthday(request):   # Обычная форма для GET запросов
#     print(request.GET)
#     form = BirthdayForm()
#     context = {'form': form}
#     return render(request, 'birthday/birthday_form.html', context=context)

# def birthday(request):
#     if request.GET:
#         form = BirthdayForm(request.GET)
#         if form.is_valid():
#             pass
#     else:
#         form = BirthdayForm(request.GET)
#     context = {'form': form}
#     return render(request, 'birthday/birthday_form.html', context=context)


# def birthday_list(request):
#     # Получаем список всех объектов с сортировкой по id.
#     birthdays = Birthday.objects.order_by('id')
#     # Создаём объект пагинатора с количеством 2(10) записей на страницу.
#     paginator = Paginator(birthdays, 2)
#     # Получаем из запроса значение параметра page.
#     page_number = request.GET.get('page')
#     # Получаем запрошенную страницу пагинатора.
#     # Если параметра page нет в запросе или его значение не приводится к числу,
#     # вернётся первая страница.
#     page_obj = paginator.get_page(page_number)
#     # Вместо полного списка объектов передаём в контекст
#     # объект страницы пагинатора
#     context = {'page_obj': page_obj}
#     # context = {'birthdays': birthdays}
#     return render(request, 'birthday/birthday_list.html', context)
#
#
# def delete_birthday(request, pk):
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     # Если был получен POST-запрос...
#     if request.method == 'POST':
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect('birthday:list')
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, 'birthday/birthday_form.html', context)
