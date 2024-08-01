#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from filer.models.foldermodels import Folder, FolderPermission
from geonode.base.admin import (
    RegionAdmin, HierarchicalKeywordAdmin,
    set_user_and_group_dataset_permission
)
from geonode.base.models import HierarchicalKeyword, Region
from geonode.documents.admin import DocumentAdmin, Document
from geonode.geoapps.admin import GeoAppAdmin, GeoApp
from geonode.groups.admin import GroupProfileAdmin
from geonode.groups.models import GroupProfile, GroupMember
from geonode.people.admin import ProfileAdmin, Profile
from geonode.people.forms import ProfileChangeForm

from delft.models import (
    HierarchicalKeywordExtension, RegionExtension, GroupProfileExtension,
    ResourceBaseExtension
)
from delft.models.preferences import SitePreferences
from delft.utils import is_user_file_manager, file_manager_group

admin.site.unregister(HierarchicalKeyword)
admin.site.unregister(Region)
admin.site.unregister(GroupProfile)
admin.site.unregister(Document)
admin.site.unregister(GeoApp)
admin.site.unregister(Profile)


def get_extension(resource):
    """Get extension."""
    try:
        try:
            resource.resourcebaseextension  # noqa
        except ResourceBaseExtension.DoesNotExist:
            pass
        extension, _ = ResourceBaseExtension.objects.get_or_create(
            resource=resource
        )
        return extension
    except AttributeError:
        pass
    return None


def toggle_feature(resource, is_featured):
    """Toggle the featured or not."""
    extension = get_extension(resource)
    if extension:
        extension.featured = is_featured
        extension.save()


def feature_to_home(modeladmin, request, resources):
    """Feature the resource to home."""
    for resource in resources:
        toggle_feature(resource, True)


def unfeature_to_home(modeladmin, request, resources):
    """Unfeature it to home."""
    for resource in resources:
        toggle_feature(resource, False)


# INLINES
class RegionExtensionInline(admin.StackedInline):
    model = RegionExtension


class HierarchicalKeywordExtensionInline(admin.StackedInline):
    model = HierarchicalKeywordExtension


class GroupProfileExtensionInline(admin.StackedInline):
    model = GroupProfileExtension


class ResourceBaseExtensionInline(admin.StackedInline):
    model = ResourceBaseExtension


# ADMINS
class AdminWithFeatured:
    def is_featured_at_home(self, resource):
        """Return colors that palette has."""
        extension = get_extension(resource)
        if extension:
            if extension.featured:
                return mark_safe(
                    '<img src="/static/admin/img/icon-yes.svg" alt="True">'
                )
        return mark_safe(
            '<img src="/static/admin/img/icon-no.svg" alt="False">'
        )

    is_featured_at_home.allow_tags = True


class RegionExtensionAdmin(RegionAdmin):
    inlines = [RegionExtensionInline]


class HierarchicalKeywordExtensionAdmin(HierarchicalKeywordAdmin):
    inlines = [HierarchicalKeywordExtensionInline]


class DocumentExtensionAdmin(DocumentAdmin):
    inlines = [ResourceBaseExtensionInline]


class GeoAppExtensionAdmin(AdminWithFeatured, GeoAppAdmin):
    list_display = GeoAppAdmin.list_display + ('is_featured_at_home',)
    inlines = [ResourceBaseExtensionInline]
    actions = GeoAppAdmin.actions + [feature_to_home, unfeature_to_home]


class GroupMemberInline(admin.TabularInline):
    model = GroupMember


class GroupProfileExtensionAdmin(GroupProfileAdmin):
    inlines = GroupProfileAdmin.inlines + [GroupProfileExtensionInline]


admin.site.register(Region, RegionExtensionAdmin)
admin.site.register(HierarchicalKeyword, HierarchicalKeywordExtensionAdmin)
admin.site.register(Document, DocumentExtensionAdmin)
admin.site.register(GeoApp, GeoAppExtensionAdmin)
admin.site.register(GroupProfile, GroupProfileExtensionAdmin)


class SitePreferencesAdmin(admin.ModelAdmin):
    """Site Preferences admin."""

    fieldsets = (
        ('', {
            'fields': (
                'google_analytics_measurement_id',
            ),
        }),
        ('Landing Page', {
            'fields': (
                'landing_page_banner',
                'landing_page_banner_title',
                'landing_page_banner_description'
            ),
        }),
        ('About Page', {
            'fields': (
                'about_page_title',
                'about_page_content'
            ),
        }),
    )


admin.site.register(SitePreferences, SitePreferencesAdmin)


class CustomProfileChangeForm(ProfileChangeForm):
    """Profile form with file manager."""
    is_file_manager = forms.BooleanField(required=False)

    @property
    def is_user_file_manager(self):
        """is user file manager"""
        return is_user_file_manager(self.instance)

    def __init__(self, *args, **kwargs):
        self.instance = None
        try:
            self.instance = kwargs['instance']
        except Exception:
            pass
        super().__init__(*args, **kwargs)
        self.fields[
            'is_file_manager'
        ].disabled = False if self.instance and not self.instance.is_superuser else True
        self.fields[
            'is_file_manager'
        ].initial = self.is_user_file_manager

    def clean_groups(self):
        is_file_manager = self.cleaned_data['is_file_manager']
        ids = list(self.cleaned_data['groups'].values_list('id', flat=True))
        if self.is_user_file_manager != is_file_manager:
            group = file_manager_group()
            if is_file_manager:
                self.cleaned_data['is_staff'] = True
                ids.append(group.id)
            else:
                ids.remove(group.id)
        return Group.objects.filter(id__in=ids)

    def save(self, commit=True):
        instance = super(CustomProfileChangeForm, self).save(commit=False)
        if self.cleaned_data['is_file_manager']:
            folder, _ = Folder.objects.get_or_create(
                name=f'{instance.username}',
                owner=instance
            )
            FolderPermission.objects.get_or_create(
                folder=folder,
                defaults={
                    'type': FolderPermission.CHILDREN,
                    'user': instance,
                    'can_read': FolderPermission.ALLOW,
                    'can_edit': FolderPermission.ALLOW,
                    'can_add_children': FolderPermission.ALLOW,
                }
            )
        return instance


def assign_as_staff(modeladmin, request, users):
    """Assign user as staff."""
    users.update(is_staff=True)


def unassign_as_staff(modeladmin, request, users):
    """Unassign user as staff."""
    group = file_manager_group()
    users.exclude(
        groups__in=[group.id]
    ).filter(is_superuser=False).update(is_staff=False)


def assign_as_file_manager(modeladmin, request, users):
    """Assign user to file manager."""
    group = file_manager_group()
    if group:
        users.update(is_staff=True)
        group.user_set.add(*users)


def unassign_as_file_manager(modeladmin, request, users):
    """Unassign user to file manager."""
    group = file_manager_group()
    if group:
        for user in users:
            user.groups.remove(group)


class CustomProfileAdmin(ProfileAdmin):
    """Custom profile with checking file manager."""
    list_display = (
        'id', 'username', 'organization',
        'email', 'first_name', 'last_name',
        'is_staff', 'is_active', 'is_file_manager'
    )
    form = CustomProfileChangeForm
    actions = [
        set_user_and_group_dataset_permission,
        assign_as_staff,
        unassign_as_staff,
        assign_as_file_manager,
        unassign_as_file_manager
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'is_file_manager', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Extended profile'), {'fields': ('organization', 'profile',
                                            'position', 'voice', 'fax',
                                            'delivery', 'city', 'area',
                                            'zipcode', 'country',
                                            'keywords')}),
    )

    def is_file_manager(self, obj: Profile):
        """Return colors that palette has."""
        if is_user_file_manager(obj):
            return mark_safe(
                '<img src="/static/admin/img/icon-yes.svg" alt="True">'
            )
        else:
            return mark_safe(
                '<img src="/static/admin/img/icon-no.svg" alt="False">'
            )

    is_file_manager.allow_tags = True


admin.site.register(Profile, CustomProfileAdmin)
