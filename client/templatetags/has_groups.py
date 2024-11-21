from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name="has_groups")
def has_groups(user, group_names):
    group_names = [group_name.strip() for group_name in group_names.split(",")]
    return user.is_superuser or user.groups.filter(name__in=group_names).exists()
