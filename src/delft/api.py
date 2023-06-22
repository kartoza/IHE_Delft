from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter
from geonode.base.api.filters import (
    DynamicSearchFilter, ExtentFilter, FavoriteFilter
)
from geonode.base.api.permissions import ResourceBasePermissionsFilter
from geonode.base.api.serializers import HierarchicalKeywordSerializer
from geonode.base.api.views import (
    HierarchicalKeywordViewSet, ResourceBaseViewSet
)
from geonode.base.models import HierarchicalKeyword
from geonode.base.views import HierarchicalKeywordAutocomplete
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend


class HierarchicalKeywordAutocompleteByParent(
    HierarchicalKeywordAutocomplete
):

    def get_queryset(self):
        qs = super(
            HierarchicalKeywordAutocompleteByParent, self
        ).get_queryset().order_by('name')

        try:
            keyword = HierarchicalKeyword.objects.get(
                slug=self.request.GET.get('parent', 'NONE')
            )
            qs = keyword.get_children()
        except HierarchicalKeyword.DoesNotExist:
            if self.request.GET.get('parent', 'NONE') == '_other':
                qs = qs.filter(depth=1, numchild=0)

        if self.q:
            qs = qs.filter(**{self.filter_arg: self.q})
        return qs


class HierarchicalKeywordSerializerByParent(HierarchicalKeywordSerializer):
    parent_slug = serializers.SerializerMethodField()

    def get_parent_slug(self, instance: HierarchicalKeyword):
        if instance.is_root() and not instance.numchild:
            return '_other'
        parent = instance.get_parent()
        return parent.slug if parent else None


class HierarchicalKeywordViewSetByParent(HierarchicalKeywordViewSet):
    """
    API endpoint that lists hierarchical keywords.
    """
    serializer_class = HierarchicalKeywordSerializerByParent

    def get_queryset(self):
        qs = HierarchicalKeyword.objects.all()

        try:
            keyword = HierarchicalKeyword.objects.get(
                slug=self.request.GET.get('parent', 'NONE')
            )
            qs = keyword.get_children()
        except HierarchicalKeyword.DoesNotExist:
            if self.request.GET.get('parent', 'NONE') == '_other':
                qs = qs.filter(depth=1, numchild=0)

        return qs


class KeywordsFilter(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        for key in request.query_params.keys():
            if 'keywords{' in key:
                keywords = request.GET.getlist(key, [])
                queryset = queryset.filter(keywords__slug__in=keywords)
        return queryset


class ResourceBaseViewSetWithKeywords(ResourceBaseViewSet):
    filter_backends = [
        DynamicFilterBackend, DynamicSortingFilter, DynamicSearchFilter,
        ExtentFilter, ResourceBasePermissionsFilter, FavoriteFilter,
        KeywordsFilter
    ]
    pass
