from django.db import models

from geonode.base.models import HierarchicalKeyword, Region
from geonode.groups.models import GroupProfile


class _ResourceExtension(models.Model):
    """Extension of resource."""

    featured = models.BooleanField(
        default=False, help_text='Show it to homepage.'
    )
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='delft/icon', null=True, blank=True)

    class Meta:
        abstract = True


class HierarchicalKeywordExtension(_ResourceExtension):
    """Extension of keyword."""

    keyword = models.OneToOneField(
        HierarchicalKeyword, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.keyword.slug


class RegionExtension(_ResourceExtension):
    """Extension of region."""

    region = models.OneToOneField(
        Region, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.region.name


class GroupProfileExtension(models.Model):
    """Extension of GroupProfile."""

    group_profile = models.OneToOneField(
        GroupProfile, on_delete=models.CASCADE
    )
    featured = models.BooleanField(
        default=False, help_text='Show it to homepage.'
    )

    def __str__(self):
        return self.group_profile.title
