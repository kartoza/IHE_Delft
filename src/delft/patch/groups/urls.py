from delft.patch.groups.views import group_member_remove
from geonode.urls import url

urlpatterns = [  # '',
    url(
        r'^group/(?P<slug>[-\w]+)/member_remove/(?P<username>.+)$',
        group_member_remove,
        name='group_member_remove'
    ),
]
