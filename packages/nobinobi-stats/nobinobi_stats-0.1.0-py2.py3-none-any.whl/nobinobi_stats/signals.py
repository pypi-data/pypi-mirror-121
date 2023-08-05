from sys import stdout

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_permissions_stats(sender, **kwargs):
    from nobinobi_daily_follow_up.models import DailyFollowUp
    content_type = ContentType.objects.get_for_model(DailyFollowUp)
    permission, created = Permission.objects.get_or_create(
        codename='view_stats',
        name='Can View Stats',
        content_type=content_type,
    )
    if created:
        stdout.write("Permission {} created successfully.\n".format(permission))

    try:
        group_admin = Group.objects.get(name="Admin")
    except Group.DoesNotExist:
        pass
    else:
        group_admin.permissions.add(permission)
        stdout.write("Permission {} added to {} successfully.\n".format(permission, group_admin))
