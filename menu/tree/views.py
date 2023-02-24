from django.shortcuts import render

from .models import Menu


def index(request):
    template = "base.html"
    return render(request, template)


def draw_menu(request, slug):

    def get_all_level(section):
        return section.top_section.down_sections.all()

    menu = Menu.objects.get(sections__slug=slug)
    current_section = menu.sections.get(slug=slug)
    down_sections = current_section.down_sections.all()

    top_sections = menu.sections.filter(top_section=None)
    active_top_sections = []
    levels = [top_sections]
    section = current_section
    while section.top_section:
        active_top_sections.append(section.top_section)
        levels.append(get_all_level(section))
        section = section.top_section
    template = "tree/menu.html"
    context = {
        'menu': menu,
        'sections': top_sections,
        'down_sections': down_sections,
        'levels': levels,
        'active_top_sections': active_top_sections
    }
    return render(request, template, context)
