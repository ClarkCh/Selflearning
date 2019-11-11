# Generated by Django 2.2.6 on 2019-10-22 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_teacher_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(choices=[('country', '全国知名'), ('world', '全球知名')], default='country', max_length=20, verbose_name='知名程度'),
            preserve_default=False,
        ),
    ]
