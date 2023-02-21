from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Section


def get_menu(request, slug):
    section = get_object_or_404(Section, slug=slug)
    template = "tree/menu.html"
    context = {
        'section': section,
    }
    return render(request, template, context)
