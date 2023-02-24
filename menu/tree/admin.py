"""
В этом модуле настроено редактирование меню
через страндартную панель администратора.
"""
from django.contrib import admin

from .models import Menu, Section

admin.site.register(Section)
admin.site.register(Menu)
