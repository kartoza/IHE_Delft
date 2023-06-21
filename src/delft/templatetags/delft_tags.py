from django import template
from geonode.base.models import HierarchicalKeyword

from delft.models import HierarchicalKeywordExtension, RegionExtension

register = template.Library()


@register.simple_tag(takes_context=True, name='get_parent_keywords')
def get_parent_keywords(context):
    """Return keyword children."""
    return HierarchicalKeyword.objects.filter(depth=1)


@register.simple_tag(takes_context=True, name='get_keyword_children')
def get_keyword_children(context, keyword_slug):
    """Return keyword children."""
    try:
        keyword = HierarchicalKeyword.objects.get(slug=keyword_slug)
        return keyword.get_tree(parent=keyword).exclude(pk=keyword.pk).filter(
            pk__in=HierarchicalKeywordExtension.objects.filter(
                featured=True
            ).values_list('keyword__id', flat=True)
        )
    except HierarchicalKeyword.DoesNotExist:
        return []


@register.simple_tag(takes_context=True, name='get_featured_regions')
def get_featured_regions(context):
    """Return featured regions."""
    regions = RegionExtension.objects.filter(featured=True)
    return regions
