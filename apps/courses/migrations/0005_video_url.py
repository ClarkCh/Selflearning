# Generated by Django 2.2.6 on 2019-10-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='www.baidu.com', max_length=200, verbose_name='视频访问地址'),
            preserve_default=False,
        ),
    ]
