# Generated by Django 2.2.6 on 2019-10-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='catgory',
            field=models.CharField(default='后端开发', max_length=20, verbose_name='课程类别'),
            preserve_default=False,
        ),
    ]