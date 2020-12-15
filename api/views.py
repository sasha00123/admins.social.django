import json
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_social_auth.views import SocialJWTPairUserAuthView

from accounts.models import Group, Post, AdsEntry
from accounts.serializers import AccountSerializer, GroupSerializer


@require_http_methods(['GET'])
def get_posts(request):
    """
        This view is used by parser to get posts and update stats
    """
    if request.GET.get('secret', '') != settings.PARSER_API_SECRET:
        return HttpResponseForbidden()
    posts = Post.objects.filter(date__gte=datetime.now() - timedelta(days=1))
    posts = [post.pid for post in posts.all()]
    return HttpResponse(json.dumps(posts))


@require_http_methods(['GET'])
def get_groups(request):
    """
        This view is used by parser to get groups and then update posts.
    """
    if request.GET.get('secret', '') != settings.PARSER_API_SECRET:
        return HttpResponseForbidden()
    ids = [group.gid for group in Group.objects.all()]
    return HttpResponse(json.dumps(ids))


def find_group(screen_name):
    """
    Useful to find ads target.
    This function searches for group in database using screen_name.
    Also tries to replace public with club, because groups without screen_name
    are stored in format: club*.

    :param screen_name: string
    :return: Group or None
    """
    alternate = screen_name
    if "public" in screen_name:
        alternate = alternate.replace("public", "club")
    try:
        group = Group.objects.filter(
            Q(screen_name=alternate) | Q(screen_name=screen_name) | Q(gid=alternate.replace("club", ""))).get()
    except Group.DoesNotExist:
        group = None
    return group


@csrf_exempt
@require_http_methods(['POST'])
def update_posts(request):
    """
        View used to update posts.
        Should only be used by parser, protected by PARSER_API_SECRET.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Wrong data format!")

    if data.get('secret', '') != settings.PARSER_API_SECRET:
        return HttpResponseForbidden("")

    for p in data['posts']:
        try:
            post = Post.objects.get(pid=p['id'])
            created = False
        except Post.DoesNotExist:
            post = Post(pid=p['id'])
            created = True

        if created:
            tz = pytz.timezone("Europe/Moscow")
            post.date = datetime.fromtimestamp(p['date'], tz=tz)
            post.group = Group.objects.get(gid=int(p['gid']))
            if p['images']:
                post.images = json.dumps(p['images'])
            post.text = p['text']

        if data['update_stats'] or created:
            post.likes = p['likes']
            post.views = p['views']
            post.shares = p['shares']
            post.save()

        if created and isinstance(p['ads'], list):
            ads = [find_group(g) for g in p['ads']]
            for g in ads:
                if g is not None and g != post.group:
                    AdsEntry.objects.get_or_create(group=g, post=post)
            post.save()

    return HttpResponse("ok")


class AccountInfo(generics.RetrieveAPIView):
    """
        Can be used to check if user token is not expired.
        Used to retrieve info about user.
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class JwtAuthView(SocialJWTPairUserAuthView):
    """
        Used to get log in and return minimal info about user.
    """
    serializer_class = AccountSerializer


class GroupView(generics.RetrieveAPIView):
    """
        View to retrieve group by gid on VK.
    """
    lookup_field = 'gid'
    lookup_url_kwarg = 'gid'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
