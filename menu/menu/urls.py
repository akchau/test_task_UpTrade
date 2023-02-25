"""
Главный модуль urls
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("test_app.urls", namespace="test_app")),
]
