from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseForbidden)
from django.shortcuts import (
    get_object_or_404,
    redirect
)
from geonode.groups.models import GroupMember, GroupProfile


@login_required
def group_member_remove(request, slug, username):
    group = get_object_or_404(GroupProfile, slug=slug)
    user = get_object_or_404(get_user_model(), username=username)

    if not group.user_is_role(request.user, role="manager"):
        return HttpResponseForbidden()
    else:
        # TODO:
        #  Delft specified
        #  Error when there is duplication group member
        group_member = GroupMember.objects.filter(
            group=group, user=user
        ).first()
        if group_member:
            group_member.delete()
        return redirect("group_detail", slug=group.slug)
