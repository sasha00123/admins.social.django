# Generated by Django 2.1.5 on 2019-04-29 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0006_profile_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.BigIntegerField()),
                ('date', models.DateTimeField()),
                ('likes', models.IntegerField()),
                ('views', models.IntegerField()),
                ('shares', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('ads', models.ManyToManyField(related_name='ads', to='accounts.Group')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts',
                                            to='accounts.Group')),
            ],
        ),
    ]
