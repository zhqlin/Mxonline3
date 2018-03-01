from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict


# Create your views here.
# 处理课程机构列表的view
class OrgView(View):
    def get(self, request):
        # 查找到所有的课程机构
        all_orgs = CourseOrg.objects.all()
        # 总共有多少家机构，采用count进行统计
        org_nums = all_orgs.count()
        # 取出所有城市
        all_citys = CityDict.objects.all()
        # 进行分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_orgs取出5个来，每页显示5个
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)


        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
        })
