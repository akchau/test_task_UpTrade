from django.urls import path

from .views import draw_menu, index

app_name = "tree"

urlpatterns = [
    path("<slug:slug>/", draw_menu, name="debug"),  # адрес cтраницы меню
    path("", index, name="index"),
]
