# Generated by Django 2.2.6 on 2019-10-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20191018_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default=2, max_length=200, upload_to='teachers/%Y/%m', verbose_name='教师封面'),
            preserve_default=False,
        ),
    ]
