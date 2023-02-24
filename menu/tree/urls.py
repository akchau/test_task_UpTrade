from django.urls import path

from .views import draw_menu, get_menu

app_name = "tree"

urlpatterns = [
    # path("<slug:slug>/", get_menu, name="menu"),  # адрес cтраницы меню
    path("<slug:slug>/", draw_menu, name="debug"),  # адрес cтраницы меню
]

