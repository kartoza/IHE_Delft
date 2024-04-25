import logging

from delft.serializer import (
    GroupProfileSerializerWithCount,
    HierarchicalKeywordSerializerByParent
)
from delft.utils import is_user_filer_url
from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter
from geonode.base.api.filters import (
    DynamicSearchFilter, ExtentFilter, FavoriteFilter
)
from geonode.base.api.permissions import ResourceBasePermissionsFilter
from geonode.base.api.views import (
    HierarchicalKeywordViewSet, ResourceBaseViewSet, GroupViewSet
)
from geonode.base.models import HierarchicalKeyword
from geonode.base.views import HierarchicalKeywordAutocomplete
from geonode.documents.api.views import (
    DocumentViewSet, DocumentPermissionsFilter
)
from geonode.groups.models import GroupProfile
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class GroupViewSetWithCount(GroupViewSet):
    """API endpoint that lists groups."""

    serializer_class = GroupProfileSerializerWithCount


class HierarchicalKeywordAutocompleteByParent(
    HierarchicalKeywordAutocomplete
):
    """API endpoint that lists hierarchical keywords."""

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
        if self.request.GET.get('is_init', False):
            qs = qs.filter(hierarchicalkeywordextension__is_initial=True)
        return qs


class HierarchicalKeywordViewSetByParent(HierarchicalKeywordViewSet):
    """API endpoint that lists hierarchical keywords."""

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
                if 'filter{slug.icontains}' not in self.request.GET.keys():
                    qs = qs.filter(
                        hierarchicalkeywordextension__is_initial=True
                    )

        return qs


class KeywordsFilter(BaseFilterBackend):
    """Filter resource by the keywords."""

    def filter_queryset(self, request, queryset, view):
        for key in request.query_params.keys():
            if 'keywords{' in key:
                keywords = request.GET.getlist(key, [])
                queryset = queryset.filter(keywords__slug__in=keywords)
        return queryset


class ByProfileFilter(BaseFilterBackend):
    """Filter resource by accessed profile."""

    def filter_queryset(self, request, queryset, view):
        for key in request.query_params.keys():
            if key == 'by-profile':
                if not request.user.is_staff:
                    queryset = queryset.filter(
                        group__in=GroupProfile.groups_for_user(
                            request.user
                        ).values_list('group')
                    )
        return queryset


class ResourceBaseViewSetWithKeywords(ResourceBaseViewSet):
    """API endpoint that allows base resources to be viewed or edited."""

    filter_backends = [
        DynamicFilterBackend, DynamicSortingFilter, DynamicSearchFilter,
        ExtentFilter, ResourceBasePermissionsFilter, FavoriteFilter,
        KeywordsFilter, ByProfileFilter
    ]


class DocumentViewSetWithProfile(DocumentViewSet):
    """API endpoint that allows base resources to be viewed or edited."""

    filter_backends = [
        DynamicFilterBackend, DynamicSortingFilter, DynamicSearchFilter,
        ExtentFilter, DocumentPermissionsFilter, ByProfileFilter
    ]


class UserFilerUrlAPI(APIView):
    """Return User Filer URL."""

    def get(self, request):
        """Return User Filer URL."""
        return Response(is_user_filer_url(request.user))
