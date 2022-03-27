from django.template.loader_tags import register


@register.filter
def split(value, key):
    return value.split(key)
