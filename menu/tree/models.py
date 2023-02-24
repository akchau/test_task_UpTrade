"""В этом модуле описана модель секции меню."""
from django.db import models


class Menu(models.Model):
    """Меню"""
    name = models.CharField(
        "Название",
        max_length=200,
        unique=True,
        help_text="Укажите название",
    )

    def __str__(self):
        return self.name


class Section(models.Model):
    """Секция меню"""
    name = models.CharField(
        "Название",
        max_length=200,
        unique=True,
        help_text="Укажите имя секции",
    )
    slug = models.SlugField(
        "Адресс секции",
        max_length=200,
        unique=True,
        help_text="Укажите адресс секции",
    )
    top_section = models.ForeignKey(
        'self',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='down_sections',
        verbose_name='Родительская секция',
        help_text='Укажите родительскую секцию'
    )

    def __str__(self):
        return self.name
