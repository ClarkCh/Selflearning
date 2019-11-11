from datetime import datetime

from django.db import models

from courses.models import Course
from users.models import UserProfile


class UserAsk(models.Model):
    '''
    用户咨询
    '''
    name = models.CharField(max_length=18, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course = models.CharField(max_length=28, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComments(models.Model):
    '''
    用户评论
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户名')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程名')
    comment = models.CharField(max_length=800, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class UserFavourite(models.Model):
    '''
    用户收藏
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户名')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程机构'), (3, '教师')), verbose_name='收藏类型')
    fav_id = models.IntegerField(default=0, verbose_name='数据ID')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    '''
    用户消息
    '''
    # 这里如果userid为零, 则向全体user发送, 其他的向对应ID发送
    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=800, verbose_name='消息内容')
    # 判断消息是否已读
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class UserCourse(models.Model):
    '''
    用户课程
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name
