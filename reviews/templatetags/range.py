from django import template

register = template.Library()


@register.filter(name="get_range")
def get_range(number: int):
    return range(1, number + 1)
