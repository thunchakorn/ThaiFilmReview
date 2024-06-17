from django import template

register = template.Library()


@register.simple_tag
def get_pagination_url(page, query):
    query = [q for q in query.split("&") if "page" not in q]
    return f"?page={page}&" + "&".join(query)
