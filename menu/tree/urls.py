from django.urls import path

from .views import get_menu

app_name = "tree"

urlpatterns = [
    path("<slug:slug>/", get_menu, name="menu"),  # адрес cтраницы меню
]