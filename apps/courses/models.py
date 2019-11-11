from datetime import datetime

from django.db import models

from ckeditor.fields import RichTextField


class Course(models.Model):
    teacher = models.ForeignKey('organization.Teacher', on_delete=models.CASCADE, verbose_name='课程讲师', null=True, blank=True)
    course_org = models.ForeignKey('organization.CourseOrg', on_delete=models.CASCADE, verbose_name='课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = RichTextField(verbose_name='课程详细')
    is_banner = models.BooleanField(default=False, verbose_name='是否广告课程')
    degree = models.CharField(max_length=20, verbose_name='课程难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')))
    learn_times = models.FloatField(default=0, verbose_name='学习时长(小时)')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    favourites = models.IntegerField(default=0, verbose_name='收藏数')
    # students = models.IntegerField(default=0, verbose_name='学生数')
    catgory = models.CharField(max_length=20, verbose_name='课程类别')
    tag = models.CharField(max_length=20, verbose_name='课程标签')
    image = models.ImageField(max_length=200, upload_to='courses/%Y/%m', verbose_name='课程封面')
    needtoknow = models.CharField(max_length=200, verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=200, verbose_name='老师告诉你')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def students(self):
        return self.usercourse_set.filter(course=self).count()

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程对应的所有章节内容
        return self.lesson_set.all()

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=88, verbose_name='章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def get_lesson_video(self):
        # 获取章节对应的所有视频内容
        return self.video_set.all()

    class Meta:
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='章节名')
    name = models.CharField(max_length=88, verbose_name='视频名')
    url = models.CharField(max_length=200, verbose_name='视频访问地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=88, verbose_name='资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='下载地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
