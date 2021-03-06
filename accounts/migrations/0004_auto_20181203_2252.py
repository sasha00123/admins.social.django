# Generated by Django 2.1.3 on 2018-12-03 19:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_profile__groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.BigIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('photo', models.CharField(max_length=255)),
                ('members', models.IntegerField()),
                ('admins', models.ManyToManyField(related_name='vk_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='_groups',
        ),
    ]
