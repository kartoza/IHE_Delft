from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

User = get_user_model()


def is_user_able_to_add(user: User):
    """Check if user is able to add resource.

    Should be superuser or user who are already in group.
    """
    return user.is_authenticated and (
            user.is_superuser or 'add_resource' in user.perms
    )


def is_user_file_manager(user: User) -> bool:
    """Check if user is able to manage file.

    Should be superuser or user who are already in group.
    """
    if not user:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True
    try:
        user.groups.get(name='file-manager')
        return True
    except Group.DoesNotExist:
        return False
