# Generated by Django 2.2.6 on 2019-10-28 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20191022_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='students',
        ),
    ]
