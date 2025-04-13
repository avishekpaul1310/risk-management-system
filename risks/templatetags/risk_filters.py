from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the arg and the value"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return None