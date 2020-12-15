from django.shortcuts import render
from django.views.generic import DetailView

# Create your views here.
from accounts.models import Group


def render_main(request):
    return render(request, "main.html")


class GroupDetail(DetailView):
    model = Group
    context_object_name = "group"
    template_name = "group.html"
    slug_field = "gid"
    slug_url_kwarg = "gid"


def Bot(request):
    return render(request, "bot.html")


def crime(request):
    return render(request, "crime.html")


def welcome(request):
    return render(request, "welcome.html")