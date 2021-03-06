#!/usr/bin/env python3
# __author__ = 'kylin'
# encoding = 'utf-8'

from django import forms

from captcha.fields import CaptchaField


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空，密码最小长度为5
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 验证码form & 注册表单form
class RegisterForm(forms.Form):
    # 此处email与前端name需保持一致
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=6)
    # 应用验证码
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 激活时验证码实现
class ActiveForm(forms.Form):
    # 激活时不对邮箱密码做验证
    # 应用验证码，自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 忘记密码验证码实现
class ForgetPwdForm(forms.Form):
    # 此email与前端name需保持一致
    email = forms.EmailField(required=True)
    # 应用验证码，自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 重置密码form实现
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)