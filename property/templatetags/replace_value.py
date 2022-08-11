from django.template.loader_tags import register


@register.filter
def replace(value):
    return str(value).replace(',', '.')

