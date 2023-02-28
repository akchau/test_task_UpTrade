"""В этом модуле описана модель секции меню."""
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class Menu(models.Model):
    """Меню"""
    name = models.CharField(
        "Название",
        max_length=200,
        help_text="Укажите название меню.",
    )
    slug = models.SlugField(
        "Адресс меню",
        max_length=200,
        unique=True,
        help_text=(
            "Укажите адресс меню.",
            "Допустимые символы 0-9 A-Z a-z - _"
            )
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class Section(models.Model):
    """Секция меню"""
    name = models.CharField(
        "Название",
        max_length=200,
        help_text="Укажите человекочитаемое имя секции меню.",
    )
    adress = models.CharField(
        "Адресс секции",
        max_length=200,
        help_text=(
            "Укажите адресс секции в формате",
            "`namespace:name`. Без кавычек."
        )
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
        try:
            reverse(self.adress)
        except NoReverseMatch:
            raise ValidationError(
                "Такого адреса нет в проекте")
        if self.top_section == self:
            raise ValidationError(
                "Ячейка не может быть родительской секцией для себя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'menu'],
                name='name_menu'
            ),
            models.UniqueConstraint(
                fields=['adress', 'menu'],
                name='adress_menu'
            )
        ]
