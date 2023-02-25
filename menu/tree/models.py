"""В этом модуле описана модель секции меню."""
from django.core.exceptions import ValidationError
from django.db import models


class Menu(models.Model):
    """Меню"""
    name = models.CharField(
        "Название",
        max_length=200,
        unique=True,
        help_text="Укажите название",
    )
    slug = models.SlugField(
        "Адресс меню",
        max_length=200,
        unique=True,
        help_text="Укажите адресс меню",
    )

    def __str__(self):
        return self.name


class Section(models.Model):
    """Секция меню"""
    name = models.CharField(
        "Название",
        max_length=200,
        unique=True,
        help_text="Укажите человекочитаемое имя секции меню.",
    )
    adress = models.CharField(
        "Адресс секции",
        max_length=200,
        unique=True,
        help_text="Укажите адресс секции без /",
        blank=True
    )
    top_section = models.ForeignKey(
        'self',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='down_sections',
        verbose_name='Родительская секция',
        help_text=('Укажите родительскую секцию. '
                   'Если родительская секция не будет '
                   'указана - секция появится в корне меню.'),
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Меню секции',
        help_text=('Укажите к какому меню относится. '
                   'Выбранная верхняя секция должна '
                   'относится к выбраному меню!'),
    )

    def clean(self):
        if (self.top_section not in self.menu.sections.all()
           and self.top_section):
            raise ValidationError(
                "Родительская секция должна быть из указанного менню")

    def __str__(self):
        return self.name
