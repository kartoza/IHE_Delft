from django import template
from geonode.base.models import HierarchicalKeyword

from delft.models import HierarchicalKeywordExtension, RegionExtension

register = template.Library()


@register.simple_tag(takes_context=True)
def get_parent_keywords(context):
    """Return parent keywords."""
    return HierarchicalKeyword.objects.filter(depth=1, numchild__gte=1)


@register.simple_tag(takes_context=True)
def get_other_parent_keyword(context):
    """Return other children."""
    return {"slug": "_other", "name": "Key-words"}


@register.simple_tag(takes_context=True)
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


@register.simple_tag(takes_context=True)
def get_keyword_children_in_list(context, keyword_slug):
    """Return keyword children."""
    try:
        keyword = HierarchicalKeyword.objects.get(slug=keyword_slug)
        query = keyword.get_tree(parent=keyword).exclude(
            pk=keyword.pk
        )
    except HierarchicalKeyword.DoesNotExist:
        query = HierarchicalKeyword.objects.none()
    if keyword_slug == '_other':
        query = HierarchicalKeyword.objects.filter(depth=1, numchild=0)
    return list(query.values_list('name', flat=True))


@register.simple_tag(takes_context=True)
def get_featured_regions(context):
    """Return featured regions."""
    regions = RegionExtension.objects.filter(featured=True)
    return regions
