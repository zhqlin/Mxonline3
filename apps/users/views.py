from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
# 用于并集运算
from django.db.models import Q

from .models import UserProfile
from .forms import LoginForm


# 重载方法，实现邮箱账号均可登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因,Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
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
        return render(request, 'login.html', {})
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