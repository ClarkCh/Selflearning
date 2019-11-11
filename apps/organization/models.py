from datetime import datetime

from django.db import models

from courses.models import Course
from ckeditor.fields import RichTextField


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市名称')
    desc = models.CharField(max_length=200, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    tag = models.CharField(max_length=20, choices=(('country', '全国知名'), ('world', '全球知名')), verbose_name='知名程度')
    catgory = models.CharField(max_length=20, verbose_name='机构类别', default='pxjg', choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')))
    desc = RichTextField(verbose_name='机构描述')
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name='所在城市')
    address = models.CharField(max_length=180, verbose_name='机构地址')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    favourites = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(max_length=200, upload_to='courses/%Y/%m', verbose_name='机构封面')
    students = models.IntegerField(default=0, verbose_name='学生数')
    courses = models.IntegerField(default=0, verbose_name='课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所在机构')
    name = models.CharField(max_length=50, verbose_name='教师名称')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=80, verbose_name='公司职位')
    points = models.CharField(max_length=88, verbose_name='教学特点')
    desc = models.CharField(max_length=300, verbose_name='机构描述')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    age = models.IntegerField(verbose_name='讲师年龄')
    favourites = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(max_length=200, upload_to='teachers/%Y/%m', verbose_name='教师封面')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def get_course_nums(self):
        return self.course_set.all().count()

    class Meta:
        verbose_name = '教师信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
