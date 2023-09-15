from django.db.models.signals import post_save
from django.dispatch import receiver
from geonode.base.models import Region
from geonode.documents.models import Document
from geonode.geoapps.models import GeoApp
from geonode.layers.models import Dataset
from geonode.maps.models import Map


def save_parent(query, region: Region):
    if region.parent:
        query.add(region.parent)
        save_parent(region.parent)


@receiver(post_save, sender=Document)
@receiver(post_save, sender=GeoApp)
@receiver(post_save, sender=Dataset)
@receiver(post_save, sender=Map)
def update_regions(sender, instance, **kwargs):
    try:
        for region in instance.regions.all():
            save_parent(instance.regions, region)
    except Exception:
        pass
