from django.urls import path

from main.views import render_main, GroupDetail, Bot, crime, welcome

urlpatterns = [
    path('', render_main, name='main'),
    path('group/<int:gid>', GroupDetail.as_view(), name='group'),
    path('bot/', Bot,  name='Bot'),
    path('crime/', crime, name='crime'),
    path('welcome/', welcome, name='welcome'),
]
