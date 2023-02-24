from django import template

register = template.Library()


@register.filter
def pop(value):
    value.pop()
    return value
