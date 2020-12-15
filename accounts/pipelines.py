from django.db import transaction
from social_core.backends.vk import VKOAuth2

from accounts.models import Profile, Group, get_user_groups


# noinspection PyUnusedLocal
@transaction.atomic
def save_profile(backend, user, response, *args, **kwargs):
    """
        Pipeline called when user log in.
        Creates profile for the first time.
        Updates groups managed by user and all other user info.
    """
    if isinstance(backend, VKOAuth2):
        if not hasattr(user, 'profile'):
            user.profile = Profile(user=user)

        user.vk_groups.clear()

        groups = get_user_groups(response["access_token"])
        for group in groups:
            if not Group.objects.filter(gid=group["id"]).exists():
                g = Group.objects.create(gid=group["id"], name=group["name"], photo=group["photo_200"],
                                         members=group["members_count"])
            else:
                g = Group.objects.get(gid=group["id"])
                g.name = group["name"]
                g.photo = group["photo_200"]
                g.members = group["members_count"]
                g.screen_name = group["screen_name"]
            g.admins.add(user)
            g.save()
        user.profile.avatar = response["photo"]
        user.profile.access_token = response["access_token"]
        user.profile.save()
