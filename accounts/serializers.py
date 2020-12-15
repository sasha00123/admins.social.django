import json

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_social_auth.serializers import JWTPairSerializer

from accounts.models import Subscription, Service, Profile, Group, Post, AdsEntry


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name',)


class PacketSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = ('name', 'services')


class SubscriptionSerializer(serializers.ModelSerializer):
    packet = PacketSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('ends', 'packet')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('avatar', 'access_token')


class ImagesField(serializers.Field):
    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        return json.dumps(data)


class ShortGroupSerializer(serializers.ModelSerializer):
    """
        Used when there's no need to return posts and ads.
    """

    class Meta:
        model = Group
        fields = ('gid', 'name', 'photo', 'members')


class ShortPostSerializer(serializers.ModelSerializer):
    images = ImagesField()
    group = ShortGroupSerializer()

    class Meta:
        model = Post
        fields = ('pid', 'date', 'likes', 'views', 'shares', 'images', 'text', 'group')


class AdsEntrySerializer(serializers.ModelSerializer):
    group = ShortGroupSerializer()
    post = ShortPostSerializer()

    class Meta:
        model = AdsEntry
        fields = ('conversion', 'group', 'post')


class PostSerializer(serializers.ModelSerializer):
    ads_entries = AdsEntrySerializer(many=True, read_only=True)
    images = ImagesField()

    class Meta:
        model = Post
        fields = ('pid', 'date', 'ads_entries', 'likes', 'views', 'shares', 'images', 'text')


class GroupSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    ads_entries = AdsEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('gid', 'name', 'photo', 'members', 'posts', 'ads_entries')


class AccountSerializer(serializers.ModelSerializer, JWTPairSerializer):
    """
        Used to retrieve personal info.
    """
    subscriptions = SubscriptionSerializer(many=True, read_only=True)
    profile = ProfileSerializer(read_only=True)
    vk_groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'subscriptions', 'profile', 'vk_groups', 'token')
