from django.db import models
from datetime import datetime


# Create your models here.
# 课程信息表
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级')
    )
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=100, verbose_name='课程描述')
    # TextField允许我们不输入长度，可以输入到无限大，暂时定义为这个类型，后续会更新为富文本类型
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2, verbose_name='课程难度')
    # 使用分钟做好后台记录（存储最小单位），前台转换
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    # 保存学习人数，点击开始学习才算
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(
        upload_to='courses/%Y/%m',
        verbose_name='封面图',
        max_length=100
    )
    # 保存点击量，点进页面就算
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 章节
class Lesson(models.Model):
    # 因为一个课程对应很多章节，所以章节表中将课程作为外键
    # 作为一个字段可以让我们知道这个章节属于哪个课程
    course = models.ForeignKey(Course, verbose_name='课程', on_delete='CASCADE')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程章节：{1}'.format(self.course, self.name)


# 每章节视频
class Video(models.Model):
    # 因为每个章节对应多个视频，所以在视频表中将章节作为外键
    # 作为一个字段，可以让我们知道这个视频属于哪个章节
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete='CASCADE')
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}章节视频：{1}'.format(self.lesson, self.name)


# 课程资源
class CourseResource(models.Model):
    # 因为一个课程可以对应很多资源，所以在课程资源表中将课程设置为外键
    # 作为一个字段可以让我们知道这个资源属于哪个课程
    course = models.ForeignKey(Course, verbose_name='课程', on_delete='CASCADE')
    name = models.CharField(max_length=100, verbose_name='资源名称')
    # 这里定义成FileFiled，在后天管理系统中就可以有直接上传的按钮
    # FileField也是一个字符串类型，需要指定最大长度
    download = models.FileField(
        upload_to='course/resource/%Y/%m',
        verbose_name='资源文件',
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程资源:{1}'.format(self.course, self.name)