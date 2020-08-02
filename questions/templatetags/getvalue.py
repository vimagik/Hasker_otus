from django import template

register = template.Library()


@register.filter(name='getvalue')
def get_value(dictionary, value):
    return dictionary.get(value)