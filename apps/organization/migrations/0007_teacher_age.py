# Generated by Django 2.2.6 on 2019-10-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=18, verbose_name='讲师年龄'),
            preserve_default=False,
        ),
    ]
