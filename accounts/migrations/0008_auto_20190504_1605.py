# Generated by Django 2.1.5 on 2019-05-04 13:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0007_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='screen_name',
            field=models.CharField(db_index=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='gid',
            field=models.BigIntegerField(db_index=True, unique=True),
        ),
    ]