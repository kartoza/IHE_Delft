from delft.models import (
    RegionExtension, GroupProfileExtension
)
from django import template
from geonode.base.models import HierarchicalKeyword, GroupProfile, ResourceBase

register = template.Library()


@register.simple_tag(takes_context=True)
def get_group_profiles(context):
    """Return group profiles keywords."""
    return GroupProfile.objects.filter(
        id__in=GroupProfileExtension.objects.filter(
            featured=True
        ).values_list('group_profile_id', flat=True)
    ).order_by('title')


@register.simple_tag(takes_context=True)
def get_parent_keywords(context):
    """Return parent keywords."""
    return HierarchicalKeyword.objects.filter(depth=1, numchild__gte=1)


@register.simple_tag(takes_context=True)
def get_other_parent_keyword(context):
    """Return other children."""
    return {"slug": "_other", "name": "Keywords"}


@register.simple_tag(takes_context=True)
def get_keyword_children(context, keyword_slug):
    """Return keyword children."""
    try:
        keyword = HierarchicalKeyword.objects.get(slug=keyword_slug)
        return keyword.get_children().filter(
            hierarchicalkeywordextension__featured=True
        ).order_by(
            'hierarchicalkeywordextension__order', 'name'
        )
    except HierarchicalKeyword.DoesNotExist:
        return []


@register.simple_tag(takes_context=True)
def get_keyword_children_in_list(context, keyword_slug):
    """Return keyword children."""
    try:
        keyword = HierarchicalKeyword.objects.get(slug=keyword_slug)
        query = keyword.get_children()
    except HierarchicalKeyword.DoesNotExist:
        query = HierarchicalKeyword.objects.none()
    if keyword_slug == '_other':
        query = HierarchicalKeyword.objects.filter(depth=1, numchild=0)
    return list(query.values_list('name', flat=True))


@register.simple_tag(takes_context=True)
def get_featured_regions(context):
    """Return featured regions."""
    regions = RegionExtension.objects.filter(
        featured=True
    ).order_by('order', 'region__name')
    return regions


@register.simple_tag(takes_context=True)
def get_featured_output(context):
    """Return featured output."""
    return ResourceBase.objects.filter(
        resourcebaseextension__featured=True
    ).order_by('resourcebaseextension__order', 'title')


@register.simple_tag(takes_context=True)
def metadata_regions(context, resource):
    """Return metadata regions."""

    parents = []
    regions = []
    for region in resource.regions.all():
        parents += [reg.code for reg in region.get_ancestors()]

    for region in resource.regions.all():
        if region.code not in parents:
            regions.append(
                [reg.name for reg in region.get_ancestors()] + [region.name]
            )
    return regions


@register.simple_tag(takes_context=True)
def replace_str(context, str, target_char, out_char):
    """Replace string."""
    return str.replace(target_char, out_char)


@register.simple_tag(takes_context=True)
def keywords(context, resource):
    """Return resource keywords in dict."""
    output = {}
    for keyword in resource.keywords.all():
        group_name = 'Keywords'
        parent = keyword.get_parent()
        if parent and parent.name:
            group_name = parent.name
        if group_name not in output:
            output[group_name] = []
        output[group_name].append(keyword)
    return output


@register.simple_tag(takes_context=True)
def delft_version(context):
    """Return version of delft."""
    return '0.0.13'
