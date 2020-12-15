from django.contrib.auth.models import User
from django.db import models

from accounts.models import Group


class Post(models.Model):
    """
        Post created on our website(auto posting).
        Used in tasks.
    """
    text = models.TextField(blank=True)


class Image(models.Model):
    """
        Image in post.
    """
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Task(models.Model):
    """
        Task is used by Auto Posting to publish posts on time.
    """
    active = models.BooleanField(default=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='task')
    time = models.DateTimeField()


class Report(models.Model):
    """
        Reports are used to show user if Task was successful or not.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reports')
    status = models.IntegerField()
    success = models.BooleanField()
    text = models.TextField()
