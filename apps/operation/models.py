from django.db import models
from datetime import datetime

# 引入CourseComments所需的外键models
from users.models import UserProfile
from courses.models import Course

# Create your models here.

# 用户咨询
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}询问《{1}》".format(self.name, self.course_name)


# 课程评价
class CourseComments(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete='CASCADE')
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete='CASCADE')
    comments = models.CharField(max_length=250, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评价'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}对《{1}》的评价'.format(self.user, self.course)


# 用户收藏（课程、讲师、机构）
class UserFavorite(models.Model):
    TYPE_CHOICES = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '讲师')
    )
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete='CASCADE')
    # 直接保存保存id
    fav_id = models.IntegerField(default=0, verbose_name='收藏ID')
    # 保存具体的收藏类型
    fav_type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name='收藏类型'
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}的{1}收藏".format(self.user, self.fav_type)


# 用户消息表
class UserMessage(models.Model):
    # 消息有两种，发送给全体和个别用户
    # 为0发送给全体，不为0发送给用户的id
    user = models.IntegerField(default=0, verbose_name='接收用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    # 是否已读
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "发送给{0}的消息".format(self.user)


# 用户课程表
class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete='CASCADE')
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete='CASCADE')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}参加的《{1}》课程'.format(self.user, self.course)