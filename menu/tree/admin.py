"""
В этом модуле настроено редактирование меню
через страндартную панель администратора.
"""
from django.contrib import admin

from .models import Menu, Section


class SectionInline(admin.TabularInline):
    model = Section


class MenuAdmin(admin.ModelAdmin):
    inlines = [
        SectionInline,
    ]
    """Отображение меню."""
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')


admin.site.register(Menu, MenuAdmin)
