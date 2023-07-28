"""Patch validation for auth model."""

from geonode.base.api.serializers import SimpleHierarchicalKeywordSerializer


def new_to_representation(self, value):
    parent = value.get_parent()
    return {
        'name': value.name,
        'slug': value.slug,
        'parent_slug': parent.slug if parent else None,
        'parent_name': parent.name if parent else None,
    }


SimpleHierarchicalKeywordSerializer.to_representation = new_to_representation
