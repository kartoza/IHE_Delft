# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from delft.models.extensions import HierarchicalKeywordExtension
from django.db import migrations
from geonode.base.models import HierarchicalKeyword


def import_data(apps, schema_editor):
    for keyword in HierarchicalKeyword.objects.all():
        obj, _ = HierarchicalKeywordExtension.objects.get_or_create(
            keyword=keyword,
            defaults={
                'featured': False
            }
        )
        obj.is_initial = True
        obj.save()


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('delft', '0007_hierarchicalkeywordextension_is_initial'),
    ]

    operations = [
        migrations.RunPython(import_data, migrations.RunPython.noop),
    ]
