from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=False)
@stringfilter
def rupluralize(value, forms):
    """
    Подбирает окончание существительному после числа
    {{someval|rupluralize:"<one>,<two>,<many>"}}

    Пример:
        {{someval|rupluralize:"товар,товара,товаров"}}

    https://gist.github.com/dpetukhov/cb82a0f4d04f7373293bdf2f491863c8
    """
    try:
        one, two, many = forms.split(u',')
        value = str(value)[-2:]  # 314 -> 14

        if (21 > int(value) > 4):
            return many

        if value.endswith('1'):
            return one
        elif value.endswith(('2', '3', '4')):
            return two
        else:
            return many

    except (ValueError, TypeError):
        return ''


@register.filter
def readable_price(number) -> str:
    """
    Разделяет тысячи с помощью пробелов
    {{someval|readable_price}}

    Args:
        number:

    Returns: str

    Examples:
        68 -> 68
        68000 -> 68 000
        68000.1 -> 68 000.1
        68000000 -> 68 000 000

    """
    return '{:,}'.format(number).replace(',', ' ')
