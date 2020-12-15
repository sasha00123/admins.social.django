from django.urls import path

from api.views import AccountInfo, JwtAuthView, GroupView, get_groups, update_posts, get_posts

urlpatterns = [
    path('login/social/jwt-pair-user/', JwtAuthView.as_view()),
    path('account-info', AccountInfo.as_view()),
    path('group/<int:gid>', GroupView.as_view()),
    path('get_groups', get_groups),
    path('get_posts', get_posts),
    path('update_posts', update_posts)
]
