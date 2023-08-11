from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from geonode.groups.models import GroupProfile

User = get_user_model()


def check_user_group(user):
    """Check user to contributor or not based on group profile they have."""
    contributor_group = Group.objects.get(name='contributors')
    if contributor_group:
        groups = user.groups.filter(
            id__in=GroupProfile.objects.all().values_list('group_id')
        )
        if groups.count():
            contributor_group.user_set.add(user)
        else:
            contributor_group.user_set.remove(user)


@receiver(post_save, sender=User)
def add_or_remove_user_as_contributor(sender, instance, **kwargs):
    """Remove or Add user as contributor
    based on the number of group profile he has."""
    check_user_group(instance)


def handle_m2m_changed(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        if instance.__class__ == User:
            check_user_group(instance)


m2m_changed.connect(handle_m2m_changed, sender=User.groups.through)
