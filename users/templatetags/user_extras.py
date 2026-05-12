from django import template


register = template.Library()


@register.filter
def compact_number(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return value

    if abs(number) >= 1_000_000:
        return f"{number / 1_000_000:.1f}".rstrip("0").rstrip(".") + "M"

    if abs(number) >= 1_000:
        return f"{number / 1_000:.1f}".rstrip("0").rstrip(".") + "K"

    return str(number)
