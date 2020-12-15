# Generated by Django 2.1.5 on 2019-04-21 21:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('async_tasks', '0002_task_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.BigIntegerField(unique=True)),
                ('image', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('members', models.IntegerField()),
                ('users', models.ManyToManyField(related_name='search_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reports',
                                    to='async_tasks.Task'),
            preserve_default=False,
        ),
    ]
