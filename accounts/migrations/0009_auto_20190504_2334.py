# Generated by Django 2.1.5 on 2019-05-04 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190504_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.AlterField(
            model_name='post',
            name='pid',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
