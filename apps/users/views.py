from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
# 用于并集运算
from django.db.models import Q

from .models import UserProfile


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
