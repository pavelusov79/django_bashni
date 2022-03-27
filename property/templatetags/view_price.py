from django.template.loader_tags import register
from django.template.defaultfilters import stringfilter


@register.filter
@stringfilter
def price(value):
    if len(value) == 5:
        price_str = f'{value[:2]} {value[2:]}'
    elif len(value) == 6:
        price_str = f'{value[:3]} {value[3:]}'
    elif len(value) == 7:
        price_str = f'{value[0]} {value[1:4]} {value[-3:]}'
    else:
        price_str = f'{value[:2]} {value[2:5]} {value[-3:]}'
    return price_str



