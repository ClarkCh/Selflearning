# Generated by Django 2.2.6 on 2019-10-28 14:59

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_courseorg_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='机构描述'),
        ),
    ]