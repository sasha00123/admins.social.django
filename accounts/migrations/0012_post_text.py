# Generated by Django 2.2.1 on 2019-05-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190516_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=100, null=True),
        ),
    ]