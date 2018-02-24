from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
# 用于并集运算
from django.db.models import Q

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetPwdForm, ModifyPwdForm
from utils.email_send import send_email


# 重载方法，实现邮箱账号均可登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因,Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# 用户登录校验
'''
#采用函数方式实现验证
def user_login(request):
    # 登录提交表单为POST
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')

        # 成功返回user对象，失败返回null
        user = authenticate(username=user_name, password=pass_word)

        if user is not None:
            # login两个参数，request和user
            # 实际上上是对request写了一部分东西进去，然后再render回去
            # 这些信息就随着返回浏览器，实现登录
            login(request, user)
            # 跳转到首页user request会被带到首页
            return render(request, 'index.html')
        else:
            # 如果认证未成功，则回到登录页面
            return render(request, 'login.html', {'msg': '用户名或密码错误！'})
    # 获取登录页面为GET
    elif request.method == 'GET':
        return render(request, 'login.html', {})
'''


# 采用类方式实现
class LoginView(View):
    # 直接调用get方法，免去判断
    def get(self, request):
        return render(request, 'login.html', {'msg':''})

    def post(self, request):
        # 自动进行字段合规性验证(来自forms中规则）
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 注册功能的view
class RegisterView(View):
    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            # 判断邮箱是否已经被注册
            all_record = UserProfile.objects.filter(email=user_name)
            if all_record:
                return render(request, 'register.html', {'msg': '该邮箱已经被注册！'})
            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            # 默认激活状态为false
            user_profile.is_active = False
            user_profile.save()
            # 发送注册激活邮件
            send_status = send_email(user_name, 'register')
            if send_status:
                return render(request, 'login.html', {'msg': '注册完成，账号激活邮件已经发送，请查收！'})
            else:
                return render(request, 'register.html', {'msg': '注册邮件发送失败！'})
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 激活用户
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查验邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        # 如果不为空也就是有用户
        if all_record:
            for record in all_record:
                # 获取对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, 'login.html', {'msg': '您的账号已激活，请登录!'})
        # 对于瞎编的验证码
        else:
            return render(request, 'register.html', {'msg': '您的激活链接无效', 'active_form': active_form})


# 忘记密码
class ForgetPwdView(View):
    # get方法直接返回页面
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        # form验证合法情况下取出email
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码邮件
            send_email(email, 'forget')
            # 发送完毕返回登录页面并显示邮件发送成功
            return render(request, 'login.html', {'msg': '重置密码邮件已发送，请注意查收！'})
        # 如果表单验证失败也就是验证码输错等
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空，也就是有用户时
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应邮箱
                email = record.email
                # 将email传递回去
                return render(request, 'password_reset.html', {'email': email})
        # 错误的验证码
        else:
            return render(request, 'forgetpwd.html', {
                'msg': '您的重置密码链接无效，请重新请求！',
                'active_form': active_form
            })


# 改变密码的view
class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致！'})
            # 如果密码一致
            user = UserProfile.objects.get(email=email)
            # 加密为密文
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html', {'msg': '密码修改成功，请登录'})
        # 验证失败说明密码位数不够
        else:
            email = request.POST.get('email','')
            return render(request, 'password_reset.html', {
                'email': email,
                'modifypwd_form': modifypwd_form
            })