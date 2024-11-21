from django.contrib.auth.models import Group

from users.domains import IGroupManager


class GroupManager(IGroupManager):
    def add_user_to_group(self, user, group_name: str) -> None:
        if not Group.objects.filter(name=group_name).exists():
            # TODO Ankit add permission files later
            pass
            # Load permissions or create group logic if necessary
            # populate_permissions_from_files()
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        user.save()
