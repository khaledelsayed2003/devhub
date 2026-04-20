from django import template
from django.utils import timezone


register = template.Library()


@register.filter
def largest_timesince(value):
    if not value:
        return ''

    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    seconds = int((timezone.now() - value).total_seconds())

    if seconds < 60:
        return 'just now'

    units = (
        ('year', 60 * 60 * 24 * 365),
        ('month', 60 * 60 * 24 * 30),
        ('week', 60 * 60 * 24 * 7),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
    )

    for unit_name, unit_seconds in units:
        amount = seconds // unit_seconds
        if amount:
            plural = '' if amount == 1 else 's'
            return f'{amount} {unit_name}{plural} ago'

    return 'just now'
