import json

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    """
        Model for VK group.
        Group can be added via parsing, special form or when admin log in.
    """
    gid = models.BigIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255, db_index=True)
    photo = models.CharField(max_length=255)
    members = models.IntegerField()

    admins = models.ManyToManyField(User, related_name="vk_groups")


class Post(models.Model):
    """
        Model existing post from VK.
        Can be added via parsing and admin log in.
    """
    pid = models.CharField(max_length=255, db_index=True)
    date = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="posts")
    ads = models.ManyToManyField(Group, through="AdsEntry", related_name='ads')
    images = models.TextField(null=True)
    text = models.CharField(max_length=100, null=True)

    likes = models.IntegerField()
    views = models.IntegerField()
    shares = models.IntegerField()


class AdsEntry(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ads_entries")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="ads_entries")
    conversion = models.PositiveIntegerField(default=0)


class Profile(models.Model):
    """
        Model for user storing custom fields retrieved from VK
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_full_name()


class Period(models.Model):
    """
        Defines time periods for Packets.
    """
    name = models.CharField(max_length=255)
    duration = models.DurationField()
    sale = models.PositiveIntegerField()


class Service(models.Model):
    """
        Defines services can be sold in Packets.
    """
    name = models.CharField(max_length=255)


class Packet(models.Model):
    """
        Model to store offers and single-service packets.
    """
    single = models.BooleanField()
    name = models.CharField(max_length=255)
    costPerMonth = models.PositiveIntegerField()

    services = models.ManyToManyField(Service, related_name='packets')
    users = models.ManyToManyField(User, through='Subscription', related_name='packets')


class Subscription(models.Model):
    """
        Model stores user subscriptions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE, related_name='subscriptions')
    ends = models.DateTimeField()


def get_user_groups(access_token):
    """
    This method allow to get groups where user is admin or editor by access_token.

    :param access_token: string
    :return: []dict
    """
    data = {
        "v": settings.VK_API_VERSION,
        "access_token": access_token,
        "filter": "admin,editor",
        "extended": True,
        "fields": "members_count",
        "count": 1000
    }

    url = "https://api.vk.com/method/groups.get"
    response = requests.post(url, data)

    if not response.ok:
        return []

    response = json.loads(response.text)

    if "response" not in response:
        return []

    return response["response"]["items"]
