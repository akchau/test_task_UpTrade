from django.urls import path

from .views import draw_menu

app_name = "tree"

urlpatterns = [
    path("<slug:slug>/", draw_menu, name="debug"),  # адрес cтраницы меню
]
