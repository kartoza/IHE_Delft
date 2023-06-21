from geonode.base.models import HierarchicalKeyword
from geonode.base.views import HierarchicalKeywordAutocomplete


class HierarchicalKeywordAutocompleteByParent(
    HierarchicalKeywordAutocomplete
):

    def get_queryset(self):
        qs = super(
            HierarchicalKeywordAutocompleteByParent, self
        ).get_queryset().order_by('pk')

        try:
            keyword = HierarchicalKeyword.objects.get(
                slug=self.request.GET.get('parent', 'NONE')
            )
            qs = keyword.get_tree(parent=keyword).exclude(pk=keyword.pk)
        except HierarchicalKeyword.DoesNotExist:
            if self.request.GET.get('parent', 'NONE') == '_other':
                qs = qs.filter(depth=1, numchild=0)

        if self.q:
            qs = qs.filter(**{self.filter_arg: self.q})
        return qs
