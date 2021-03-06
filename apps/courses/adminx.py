#!/usr/bin/env python3
# __author__ = 'kylin'
# encoding = 'utf-8'

from .models import Course, Lesson, Video, CourseResource
import xadmin


class CourseAdmin(object):
    list_display = [
        'name',
        'desc',
        'detail',
        'degree',
        'learn_times',
        'students'
    ]
    search_fields = [
        'name',
        'desc',
        'detail',
        'degree',
        'students'
    ]
    list_filter = [
        'name',
        'desc',
        'detail',
        'degree',
        'learn_times',
        'students'
    ]


class LessonAdmin(object):
    # __name代表使用外键中的name字段
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)