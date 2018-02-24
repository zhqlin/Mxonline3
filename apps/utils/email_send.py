#!/usr/bin/env python3
# __author__ = 'kylin'
# encoding = 'utf-8'

from random import Random
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import loader

from users.models import EmailVerifyRecord
from mxonline3.settings import EMAIL_FROM


def random_str(random_length=8):
    str=''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_email(email, send_type='register'):
    # 发送之前保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机code放入链接
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件内容
    if send_type == 'register':
        email_title = 'hotpig慕课小站 注册激活链接'
        email_body = '请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}'.format(code)
        # 使用Django内置函数完成邮件发送，四个参数：主题、邮件内容、从哪里发、接收者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        # if send_status:
        #     pass
        return send_status
    elif send_type == 'forget':
        email_title = 'hotpig慕课小站 找回密码链接'
        email_body = loader.render_to_string(
            'email_forget.html',
            {
                'active_code': code
            }
        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = 'html'
        send_status = msg.send()
        return send_status