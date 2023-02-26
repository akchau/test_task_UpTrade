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


class SectionAdmin(admin.ModelAdmin):
    """Отображение секции меню."""
    empty_value_display = 'root'
    list_display = (
        'name',
        'adress',
        'top_section',
        'menu',
    )
    search_fields = ('name', 'adress', 'top_section', 'menu')
    list_filter = ('menu',)


admin.site.register(Section, SectionAdmin)
admin.site.register(Menu, MenuAdmin)
