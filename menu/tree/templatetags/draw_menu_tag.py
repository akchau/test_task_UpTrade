from django import template
from django.shortcuts import render

from ..models import Menu

register = template.Library()


@register.filter
def pop(value):
    value.pop()
    return value


@register.inclusion_tag("tree/menu.html", takes_context=True)
def draw_menu(context, slug):

    def get_all_level(section):
        return section.top_section.down_sections.all()
    request = context['request']
    menu = Menu.objects.get(slug=slug)
    try:
        current_section = menu.sections.get(slug=request.path.replace("/", ""))
        down_sections = current_section.down_sections.all()
        sections = menu.sections.filter(top_section=None)
        active_top_sections = []
        levels = [sections]
        section = current_section
        while section.top_section:
            active_top_sections.append(section.top_section)
            levels.append(get_all_level(section))
            section = section.top_section
    except:
        sections = menu.sections.filter(top_section=None)
        down_sections = None
        levels = [sections]
        active_top_sections = []
    context = {
        'menu': menu,
        'sections': sections,
        'down_sections': down_sections,
        'levels': levels,
        'active_top_sections': active_top_sections
    }
    return context
