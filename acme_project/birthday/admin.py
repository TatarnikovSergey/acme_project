from django.contrib import admin
from .models import Birthday, Tag

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'birthday'
    )

    verbose_name = 'Дни рождения'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)

