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
