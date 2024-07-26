"""Patch validation for auth model."""

import logging

from django.contrib.auth.models import Permission
from geonode.base.models import Configuration
from geonode.people.models import Profile
from geonode.security.permissions import (
    READ_ONLY_AFFECTED_PERMISSIONS
)

PERMISSIONS = {
    'add_resourcebase': 'add_resource',
    'add_file': 'add_file', 'change_file': 'change_file',
    'delete_file': 'delete_file', 'view_file': 'view_file',
    'add_folder': 'add_folder', 'change_folder': 'change_folder',
    'delete_folder': 'delete_folder',
    'view_folder': 'view_folder',
    'can_use_directory_listing': 'can_use_directory_listing'
}

logger = logging.getLogger(__name__)


@property
def perms(self):
    if self.is_superuser or self.is_staff:
        # return all permissions for admins
        perms = PERMISSIONS.values()
    else:
        user_groups = self.groups.values_list('name', flat=True)
        group_perms = Permission.objects.filter(
            group__name__in=user_groups
        ).distinct().values_list('codename', flat=True)
        # return constant names defined by GeoNode
        perms = [PERMISSIONS[db_perm] for db_perm in group_perms]

    # check READ_ONLY mode
    config = Configuration.load()
    if config.read_only:
        # exclude permissions affected by readonly
        perms = [perm for perm in perms if
                 perm not in READ_ONLY_AFFECTED_PERMISSIONS]
    return perms


Profile.perms = perms
