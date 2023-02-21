"""
В этом модуле настроено редактирование меню
через страндартную панель администратора.
"""
from django.contrib import admin

from .models import Section

admin.site.register(Section)
