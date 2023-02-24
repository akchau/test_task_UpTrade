from django.shortcuts import render

from .models import Menu


def draw_menu(request, slug):

    def get_all_level(section):
        return section.top_section.down_sections.all()

    menu = Menu.objects.get(sections__slug=slug)
    current_section = menu.sections.get(slug=slug)
    down_sections = current_section.down_sections.all()

    sections = menu.sections.filter(top_section=None)
    active_top_sections = []
    levels = [sections]
    section = current_section
    while section.top_section:
        active_top_sections.append(section.top_section)
        levels.append(get_all_level(section))
        section = section.top_section
    print(levels)
    print(active_top_sections)
    template = "tree/menu.html"
    context = {
        'menu': menu,
        'sections': sections,
        'down_sections': down_sections,
        'levels': levels,
        'active_top_sections': active_top_sections
    }
    return render(request, template, context)
