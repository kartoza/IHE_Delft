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

from delft.models import (
    HierarchicalKeywordExtension, RegionExtension, GroupProfileExtension,
    ResourceBaseExtension
)
from delft.models.preferences import SitePreferences
from django.contrib import admin
from geonode.base.admin import RegionAdmin, HierarchicalKeywordAdmin
from geonode.base.models import HierarchicalKeyword, Region
from geonode.documents.admin import DocumentAdmin, Document
from geonode.geoapps.admin import GeoApp
from geonode.groups.admin import GroupProfileAdmin
from geonode.groups.models import GroupProfile, GroupMember

admin.site.unregister(HierarchicalKeyword)
admin.site.unregister(Region)
admin.site.unregister(GroupProfile)
admin.site.unregister(Document)
admin.site.unregister(GeoApp)


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
class RegionExtensionAdmin(RegionAdmin):
    inlines = [RegionExtensionInline]


class HierarchicalKeywordExtensionAdmin(HierarchicalKeywordAdmin):
    inlines = [HierarchicalKeywordExtensionInline]


class DocumentExtensionAdmin(DocumentAdmin):
    inlines = [ResourceBaseExtensionInline]


class GeoAppExtensionAdmin(DocumentAdmin):
    inlines = [ResourceBaseExtensionInline]


class GroupMemberInline(admin.TabularInline):
    model = GroupMember


class GroupProfileExtensionAdmin(GroupProfileAdmin):
    inlines = [GroupProfileExtensionInline, GroupMemberInline]


admin.site.register(Region, RegionExtensionAdmin)
admin.site.register(HierarchicalKeyword, HierarchicalKeywordExtensionAdmin)
admin.site.register(Document, DocumentExtensionAdmin)
admin.site.register(GeoApp, GeoAppExtensionAdmin)
admin.site.register(GroupProfile, GroupProfileExtensionAdmin)


class SitePreferencesAdmin(admin.ModelAdmin):
    """Site Preferences admin."""

    fieldsets = (
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
