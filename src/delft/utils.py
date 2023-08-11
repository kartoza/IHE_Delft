from django.contrib.auth import get_user_model

User = get_user_model()


def is_user_able_to_add(user: User):
    """Check if user is able to add resource.

    Should be superuser or user who are already in group.
    """
    return user.is_authenticated and (
            user.is_superuser or 'add_resource' in user.perms
    )
