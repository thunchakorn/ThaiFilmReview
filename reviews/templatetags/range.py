from django import template

register = template.Library()


@register.filter(name="get_range")
def get_range(number: int, step=1):
    return range(1, number + 1, step)


@register.inclusion_tag("reviews/inclusions/overall_rating.html")
def show_overall_rating(overall_rating):
    return {"overall_rating": overall_rating}
