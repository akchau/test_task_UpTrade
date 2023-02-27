"""Модуль с кастомными тегами для отрисовки меню."""
from django import template

from ..models import Menu

register = template.Library()


@register.filter
def pop(value):
    """
    Вспомогательный фильтр для списка уровней активных разделов,
    который позволяет удалить последний Queryset после отрисовки.
    """
    value.pop()
    return value


@register.inclusion_tag("tree/menu.html", takes_context=True)
def draw_menu(context, slug):
    """Тег включения, который отрисовывает меню."""

    def get_all_level(section):
        """
        Вспомогательная функция,
        которая возвращает все секции меню дочерние
        для передаваемой секции
        """
        return section.top_section.down_sections.all()

    # делаем запрос к БД
    menu = Menu.objects.get(slug=slug)

    # первым будут отрисованы верхние секции
    # сразу сохраним их в переменную sections
    # если страница не зарегестрирована через админку
    # то отрисовываем только верхние секции
    sections = menu.sections.filter(top_section=None)

    # на случай, если не найдется активной секции
    down_sections = None
    active_top_sections = []
    levels = []
    current_section = None
    # получаем данные о запросе для определения активной секции
    request = context['request']
    # ищем активную секцию
    if menu.sections.filter(
            adress=request.resolver_match.view_name).exists():

        # если нашли получаем сохраняем ее
        current_section = menu.sections.get(
            adress=request.resolver_match.view_name)
        # получае нижниий уровень для отрисовки
        down_sections = current_section.down_sections.all()

        # получаем список queryset-ов соответсвующих каждому уровню
        # сохраняем их в список levels
        # в этом списке будут все уровни кроме верхнего
        # он уже находится в переменной sections
        # остальные уровни будут передаваться в переменную sections
        # вместе с рекурсивным вызовом шаблона
        # в список active_top_sections сохраняем верхние
        # секции которые будут выделены как активные
        section = current_section
        while section.top_section:
            active_top_sections.append(section.top_section)
            levels.append(get_all_level(section))
            section = section.top_section

    context = {
        'name': menu.name,  # для отрисовки заголовка меню

        # в эту переменную будут передаваться уровни меню
        # при рекурсивном вызове шаблона tree
        # при первом вызове в ней упакован верхний уровень меню
        'sections': sections,

        # нижний уровень активной секции
        'down_sections': down_sections,

        # верхние уровни относительно активного
        'levels': levels,

        # секции которые будут выделены как активные кроме текущей
        'active_top_sections': active_top_sections,

        # текущая секция
        'current_section': current_section,
    }
    return context
