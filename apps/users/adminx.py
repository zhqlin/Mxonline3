#!/usr/bin/env python3
# __author__ = 'kylin'
# encoding = 'utf-8'

import xadmin

from .models import EmailVerifyRecord, Banner

# 创建EmailVerifyRecord的管理类，不再集成admin，而是集成object
class EmailVerifyRecordAdmin(object):
    # 配置后台显示列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 配置搜索列
    search_fields = ['code', 'email', 'send_type']
    # 配置筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


# 创建Banner的管理类
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)