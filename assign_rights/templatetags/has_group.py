from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Checks whether a user is in a specific group.

    Args:
        group_name(str): a string representation of a group's name
    Returns:
        boolean: True or False depending on whether user belongs to a group.
    """
    return user.groups.filter(name=group_name).exists()
