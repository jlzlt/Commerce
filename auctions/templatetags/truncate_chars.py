from django import template

register = template.Library()

@register.filter
def truncatechars(value, max_length):
    if len(value) > max_length:
        return f"{value[:max_length]}..."
    return value