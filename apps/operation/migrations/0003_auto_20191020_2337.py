# Generated by Django 2.2.6 on 2019-10-20 23:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0007_auto_20191020_2248'),
        ('operation', '0002_auto_20191020_1928'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserComments',
            new_name='CourseComments',
        ),
    ]
