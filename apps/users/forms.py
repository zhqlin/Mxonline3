#!/usr/bin/env python3
# __author__ = 'kylin'
# encoding = 'utf-8'


from django import forms


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空，密码最小长度为5
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)