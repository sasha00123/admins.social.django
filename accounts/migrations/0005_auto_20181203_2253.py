# Generated by Django 2.1.3 on 2018-12-03 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20181203_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='gid',
            field=models.BigIntegerField(unique=True),
        ),
    ]