from geonode.base.api.serializers import SimpleRegionSerializer
from geonode.base.models import Region


def get_parent(instance: Region):
    parents = get_parent(instance.parent) if instance.parent else []
    return [{
        'code': instance.code,
        'name': instance.name,
    }] + parents


def new_to_representation(self, instance):
    data = super(SimpleRegionSerializer, self).to_representation(instance)
    data['parents'] = get_parent(instance.parent) if instance.parent else []
    data['parents'].reverse()
    return data


SimpleRegionSerializer.to_representation = new_to_representation
