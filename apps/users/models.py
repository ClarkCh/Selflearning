from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, default='', verbose_name='用户昵称')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=8, verbose_name='性别', choices=(('male', '男'), ('female', '女')), default='male')
    address = models.CharField(max_length=50, verbose_name='地址', default='', null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机')
    image = models.ImageField(max_length=200, default='image/default.png', upload_to='image/%Y/%m', verbose_name='用户头像')

    def get_unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=28, choices=(('register', '注册密码'), ('forget', '找回密码'), ('change', '修改邮箱')), verbose_name='发送类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图')
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='轮播图序号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
