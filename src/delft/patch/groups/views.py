from actstream.models import Action
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseForbidden)
from django.shortcuts import (
    get_object_or_404,
    redirect)
from geonode.groups.models import GroupMember, GroupProfile
from geonode.groups.views import GroupActivityView


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


class GroupActivityHasStoryView(GroupActivityView):
    def get_context_data(self, **kwargs):
        def getKey(action):
            return action.timestamp

        def get_actions(model, ):
            actions = Action.objects.filter(
                public=True,
                action_object_content_type__model=model
            )
            actions = [
                action for action in actions if
                action.action_object and action.action_object.group == self.group.group
            ]
            return actions[:15]

        context = super().get_context_data(**kwargs)

        action_list = []

        context['action_list_datasets'] = get_actions('dataset')
        action_list.extend(context['action_list_datasets'])

        context['action_list_maps'] = get_actions('map')
        action_list.extend(context['action_list_maps'])

        context['action_list_documents'] = get_actions('document')
        action_list.extend(context['action_list_documents'])

        context['action_list_geoapps'] = get_actions('geoapp')
        action_list.extend(context['action_list_geoapps'])
        context['action_list'] = sorted(action_list, key=getKey, reverse=True)
        return context
