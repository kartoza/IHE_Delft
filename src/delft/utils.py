from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from filer.models.foldermodels import FolderPermission

User = get_user_model()


def is_user_able_to_add(user: User):
    """Check if user is able to add resource.

    Should be superuser or user who are already in group.
    """
    return user.is_authenticated and (
            user.is_superuser or 'add_resource' in user.perms
    )


FILE_MANAGER_GROUP = 'file-manager'


def file_manager_group() -> Group:
    """Return group of filemanager."""
    try:
        group, created = Group.objects.get_or_create(name=FILE_MANAGER_GROUP)

        if created:
            codenames = [
                'add_file', 'change_file', 'delete_file', 'view_file',
                'add_folder', 'change_folder', 'delete_folder',
                'view_folder', 'can_use_directory_listing'
            ]
            for codename in codenames:
                try:
                    group.permissions.add(
                        Permission.objects.get(codename=codename)
                    )
                except Permission.DoesNotExist:
                    pass
        return group
    except Group.DoesNotExist:
        return None


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
        user.groups.get(name=FILE_MANAGER_GROUP)
        return True
    except Group.DoesNotExist:
        return False


def is_user_filer_url(user: User) -> str:
    """Return user filer url."""
    if is_user_file_manager(user):
        if user.is_superuser:
            return f'/en-us/admin/filer/folder/'
        permission = FolderPermission.objects.filter(
            user=user,
            can_edit=FolderPermission.ALLOW
        ).first()
        if permission:
            folder = permission.folder
            return f'/en-us/admin/filer/folder/{folder.id}/list/'
        else:
            return f'/en-us/admin/filer/folder/'
    return None
