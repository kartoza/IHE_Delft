import logging

from geonode.base.api.serializers import (
    HierarchicalKeywordSerializer, GroupProfileSerializer
)
from geonode.base.models import HierarchicalKeyword
from geonode.groups.models import GroupProfile
from geonode.security.utils import get_resources_with_perms
from rest_framework import serializers
from rest_framework.reverse import NoReverseMatch

logger = logging.getLogger(__name__)


class GroupProfileSerializerWithCount(GroupProfileSerializer):
    """Group profile serializer."""

    def to_representation(self, instance: GroupProfile):
        request = self.context.get('request')
        filter_options = {}
        if request.query_params:
            filter_options = {
                'type_filter': request.query_params.get('type'),
                'title_filter': request.query_params.get('title__icontains')
            }
        data = super().to_representation(instance)
        if not isinstance(data, int):
            try:
                count_filter = {'group': instance.group}
                data['count'] = get_resources_with_perms(
                    request.user, filter_options
                ).filter(**count_filter).count()
            except (TypeError, NoReverseMatch) as e:
                logger.exception(e)
        return data


class HierarchicalKeywordSerializerByParent(HierarchicalKeywordSerializer):
    """Hierachical keywords serializer.."""
    parent_slug = serializers.SerializerMethodField()

    def get_parent_slug(self, instance: HierarchicalKeyword):
        if instance.is_root() and not instance.numchild:
            return '_other'
        parent = instance.get_parent()
        return parent.slug if parent else None
