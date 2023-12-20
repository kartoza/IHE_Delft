import datetime
import logging
import re
import traceback
import uuid

from django.conf import settings
from django.contrib.gis.geos import (
    GEOSGeometry)
from django.utils import timezone
from geonode.base.models import (
    Region,
    License,
    ResourceBase)
from geonode.layers.models import Dataset
from geonode.people.utils import get_valid_user
from geonode.resource import utils
from geonode.utils import OGC_Servers_Handler

logger = logging.getLogger(__name__)

ogc_settings = OGC_Servers_Handler(settings.OGC_SERVER)['default']


def new_metadata_post_save(instance, *args, **kwargs):
    logger.debug("handling UUID In pre_save_dataset")
    defaults = {}
    if isinstance(instance, Dataset) and hasattr(settings,
                                                 'LAYER_UUID_HANDLER') and settings.LAYER_UUID_HANDLER != '':
        logger.debug("using custom uuid handler In pre_save_dataset")
        from geonode.layers.utils import get_uuid_handler
        _uuid = get_uuid_handler()(instance).create_uuid()
        if _uuid != instance.uuid:
            instance.uuid = _uuid
            Dataset.objects.filter(id=instance.id).update(uuid=_uuid)

    # Set a default user for accountstream to work correctly.
    if instance.owner is None:
        instance.owner = get_valid_user()

    if not instance.uuid:
        instance.uuid = str(uuid.uuid4())

    # set default License if no specified
    if instance.license is None:
        license = License.objects.filter(name="Not Specified")
        if license and len(license) > 0:
            instance.license = license[0]

    instance.thumbnail_url = instance.get_real_instance().get_thumbnail_url()
    instance.csw_insert_date = datetime.datetime.now(
        timezone.get_current_timezone())
    instance.set_missing_info()

    defaults = dict(
        uuid=instance.uuid,
        owner=instance.owner,
        license=instance.license,
        alternate=instance.alternate,
        thumbnail_url=instance.thumbnail_url,
        csw_insert_date=instance.csw_insert_date
    )

    # Fixup bbox
    if instance.bbox_polygon is None:
        instance.set_bbox_polygon((-180, -90, 180, 90), 'EPSG:4326')
        defaults.update(
            dict(
                srid='EPSG:4326',
                bbox_polygon=instance.bbox_polygon,
                ll_bbox_polygon=instance.ll_bbox_polygon
            )
        )
    if instance.ll_bbox_polygon is None:
        instance.set_bounds_from_bbox(
            instance.bbox_polygon,
            instance.srid or instance.bbox_polygon.srid
        )
        defaults.update(
            dict(
                srid=instance.srid,
                bbox_polygon=instance.bbox_polygon,
                ll_bbox_polygon=instance.ll_bbox_polygon
            )
        )

    ResourceBase.objects.filter(id=instance.id).update(
        **defaults
    )

    try:
        if not instance.regions or instance.regions.count() == 0:
            srid1, wkt1 = instance.geographic_bounding_box.split(";")
            srid1 = re.findall(r'\d+', srid1)

            poly1 = GEOSGeometry(wkt1, srid=int(srid1[0]))
            poly1.transform(4326)

            queryset = Region.objects.all().order_by('name')
            global_regions = []
            regions_to_add = []
            for region in queryset:
                try:
                    srid2, wkt2 = region.geographic_bounding_box.split(";")
                    srid2 = re.findall(r'\d+', srid2)

                    poly2 = GEOSGeometry(wkt2, srid=int(srid2[0]))
                    poly2.transform(4326)

                    if poly2.intersection(poly1):
                        regions_to_add.append(region)
                    # TODO:
                    #  We don't need to create global region now
                    # if region.level == 0 and region.parent is None:
                    #     global_regions.append(region)
                except Exception:
                    tb = traceback.format_exc()
                    if tb:
                        logger.debug(tb)
            if regions_to_add or global_regions:
                if regions_to_add and len(
                        regions_to_add) > 0 and len(regions_to_add) <= 30:
                    instance.regions.add(*regions_to_add)
                else:
                    instance.regions.add(*global_regions)
    except Exception:
        tb = traceback.format_exc()
        if tb:
            logger.debug(tb)
    finally:
        # refresh catalogue metadata records
        from geonode.catalogue.models import catalogue_post_save
        catalogue_post_save(instance=instance, sender=instance.__class__)


utils.metadata_post_save = new_metadata_post_save
