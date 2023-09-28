from django.conf import settings
from django.forms.models import model_to_dict
from geonode.api.resourcebase_api import CommonModelApi
from geonode.base.api.serializers import (
    SimpleRegionSerializer, ResourceBaseSerializer
)


def region_to_representation(self, instance):
    data = super(SimpleRegionSerializer, self).to_representation(instance)
    data['parents'] = [{
        'code': parent.code,
        'name': parent.name,
    } for parent in instance.get_ancestors()]
    return data


SimpleRegionSerializer.to_representation = region_to_representation


def resource_base_to_representation(self, instance):
    data = super(ResourceBaseSerializer, self).to_representation(instance)
    try:
        data['maintenance_frequency_title'] = \
            instance.maintenance_frequency_title().replace('Data', 'Output')
    except IndexError:
        pass
    data['language_title'] = instance.language_title()
    return data


ResourceBaseSerializer.to_representation = resource_base_to_representation


def new_format_objects(self, objects):
    """
    Format the objects for output in a response.
    """
    for key in ('site_url', 'has_time'):
        if key in self.VALUES:
            idx = self.VALUES.index(key)
            del self.VALUES[idx]

    # hack needed because dehydrate does not seem to work in CommonModelApi
    formatted_objects = []
    for obj in objects:
        formatted_obj = model_to_dict(obj, fields=self.VALUES)
        if 'site_url' not in formatted_obj or len(
                formatted_obj['site_url']) == 0:
            formatted_obj['site_url'] = settings.SITEURL

        formatted_obj['owner__username'] = obj.owner.username
        formatted_obj['detail_url'] = obj.detail_url
        formatted_obj[
            'owner_name'] = obj.owner.get_full_name() or obj.owner.username

        if formatted_obj.get('metadata', None):
            formatted_obj['metadata'] = [
                model_to_dict(_m) for _m in formatted_obj['metadata']]

        formatted_objects.append(formatted_obj)

    return formatted_objects


CommonModelApi.format_objects = new_format_objects
