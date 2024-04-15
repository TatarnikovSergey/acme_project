# acme_project/urls.py
# Импортируем настройки проекта.
from django.conf import settings
# Импортируем функцию, позволяющую серверу разработки отдавать файлы.
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
# Добавьте новые строчки с импортами классов для регистрации пользователя.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    # Подключаем urls.py приложения для работы с пользователями.
    path('auth/', include('django.contrib.auth.urls')),
    path('birthday/', include('birthday.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
                          template_name='registration/registration_form.html',
                          form_class=UserCreationForm,
                          success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
]

# переопределяем вьюшку для ошибки 404:
handler404 = 'core.views.page_not_found'

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)


# В конце добавляем к списку вызов функции static(пока проектируем!!!).
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
