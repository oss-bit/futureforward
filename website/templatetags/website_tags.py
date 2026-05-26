from django import template

register = template.Library()


@register.filter
def mod_six(value):
    """Returns 1-6 cycling value for card gradient classes."""
    try:
        return ((int(value) - 1) % 6) + 1
    except (ValueError, TypeError):
        return 1


@register.filter
def mod_two_delay(value):
    """Returns 0, 0.08, 0.16 cycling transition delay."""
    try:
        delays = [0, 0.08, 0.16]
        return delays[(int(value)) % 3]
    except (ValueError, TypeError):
        return 0


@register.filter
def multiply_by(value, arg):
    """Multiplies value by arg for transition delays."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def slice_after_words(value, n):
    """Returns words after the first n words."""
    try:
        words = str(value).split()
        n = int(n)
        return ' '.join(words[n:]) if len(words) > n else ''
    except (ValueError, TypeError):
        return value


@register.filter
def filter_published(queryset):
    """Filter a queryset to published posts only."""
    try:
        return queryset.filter(status='published')
    except Exception:
        return queryset
