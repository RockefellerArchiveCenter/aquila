from datetime import date

from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    """Checks whether a user is in a specific group.

    Args:
        group_name(str): a string representation of a group's name
    Returns:
        boolean: True or False depending on whether user belongs to a group.
    """
    return user.groups.filter(name=group_name).exists()


@register.filter
def isoformat_date_or_string(value):
    if isinstance(value, date):
        return value.isoformat()
    else:
        return value
