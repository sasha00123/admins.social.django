import json
from datetime import timedelta
from urllib.parse import urlencode

import requests
from django.utils import timezone

from .models import Task, Report

VK_BASE = "https://api.vk.com/method"


def execute_task(task: Task):
    gid = task.group.gid

    access_token = task.creator.profile.access_token
    # TODO: check access token

    images_links = []

    # Getting image upload url
    response = requests.get("{}/{}?{}".format(VK_BASE, "photos.getWallUploadServer", urlencode({
        "access_token": access_token,
        "v": "5.78",
        "group_id": gid
    })))
    if not response.ok:
        return "Error while getting image upload server. VK returned error code.".format(response.status_code)
    response = json.loads(response.text)
    if "error" in response:
        return "Error while getting image upload server. {}".format(response["error"])

    upload_url = response["response"]["upload_url"]

    # Uploading images
    for image in task.post.images.all():
        response = requests.post(upload_url, files={
            "photo": open(image.image.path, 'rb'),
        })
        if not response.ok:
            return "Error while uploading post images. VK returned error code {}.".format(response.status_code)
        response = json.loads(response.text)
        if "error" in response:
            return "Error while uploading post images. {}".format(response['error'])

        response = requests.post("{}/{}".format(VK_BASE, "photos.saveWallPhoto"), data={
            "access_token": access_token,
            "v": "5.78",
            "group_id": gid,
            **response
        })

        if not response.ok:
            return "Error while saving post images. VK returned error code {}".format(response.status_code)
        response = json.loads(response.text)
        if "error" in response:
            return "Error while saving post images. {}".format(response["error"])

        response = response["response"][0]
        images_links.append("photo{}_{}".format(response["owner_id"], response["id"]))

    # Creating post

    response = requests.post("{}/{}".format(VK_BASE, "wall.post"), data={
        "owner_id": -gid,
        "from_group": 1,
        "message": task.post.text,
        "attachments": ",".join(images_links),
        "access_token": access_token,
        "v": "5.78",
    })

    if not response.ok:
        return "Error while saving post. VK returned error code {}".format(response.status_code)
    response = json.loads(response.text)
    if "error" in response:
        return "Error while saving post. {}".format(response.status_code)

    return "OK"


def run_tasks(stdout):
    """
        This is used to execute all pending tasks.
        Creates reports.
    """
    tasks = Task.objects.filter(time__lte=timezone.now() + timedelta(minutes=30), active=True)
    stdout.write("Working on {} tasks".format(len(tasks)))
    for task in tasks.all():
        status = execute_task(task)
        if status == "OK":
            task.active = False
            task.save()
            Report.objects.create(task=task, status=0, success=True, text=status)
        else:
            Report.objects.create(task=task, status=-1, success=False, text=status)
        stdout.write(status)
