from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render

from .models import Section


def get_menu(request, slug):

    def get_all_level(section):
        return section.top_section.down_sections.exclude(slug=slug)

    section = get_object_or_404(Section, slug=slug)
    current_section = section  # запоминаем запрошенную секцию меню
    # запоминаем следующий уровень
    down_sections = current_section.down_sections.all()
    # пустой лист для упаковки секций
    tree = []
    # получаем верхнюю часть дерева если она есть
    # начинаем обход с уровня выше запрашиваемого
    while section.top_section:
        tree.append(get_all_level(section))
        section = section.top_section
    # получаем верхний уровень
    tree.append(get_list_or_404(Section, top_section=None))
    template = "tree/menu.html"
    context = {
        'current_section': current_section,
        'tree': tree,
        'down_sections': down_sections,
    }
    return render(request, template, context)
