from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import *
from .forms import UserAskForm
from operation.models import UserFavourite


class OrgView(View):
    '''
    课程机构的首页
    '''
    def get(self, request):
        # 对课程机构进行分页并计数和筛选以及按类别排序
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = CourseOrg.objects.order_by('-click_nums')[:3]
        # 搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_orgs = CourseOrg.objects.filter(
                Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))
        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city=int(city_id))
        # 类别筛选
        catgory = request.GET.get('ct', '')
        if catgory:
            all_orgs = all_orgs.filter(catgory=catgory)
        org_nums = all_orgs.count()
        # 按类别排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            else:
                all_orgs = all_orgs.order_by('-courses')
        # 通过pure_pagination进行分页的核心操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_citys': all_citys,
            'all_orgs': orgs,
            'org_nums': org_nums,
            'city_id': city_id,
            'catgory': catgory,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class AddAskView(View):
    '''
    用户添加课程咨询
    '''
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        return HttpResponse("{'status': 'fail', 'msg':'添加出错'}", content_type='application/json')


class OrgHomeView(View):
    '''
    课程机构主页
    '''
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=org_id)
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgCourseView(View):
    '''
    课程机构内部的课程页
    '''
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()[:3]
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    '''
    课程机构内部的机构描述页
    '''
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=org_id)
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page
        })


class OrgTeacherView(View):
    '''
    课程机构内部的机构讲师页
    '''
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=org_id)
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers': all_teachers,
            'current_page': current_page
        })


class AddFavView(View):
    '''
    用户收藏和取消收藏功能
    '''
    def post(self, request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')
        if request.user.is_authenticated:
            exist_records = UserFavourite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if fav_type == '1':
                ty = Course.objects.get(id=int(fav_id))
            elif fav_type == '2':
                ty = CourseOrg.objects.get(id=int(fav_id))
            else:
                ty = Teacher.objects.get(id=int(fav_id))
            if exist_records:
                ty.favourites -= 1
                ty.save()
                # 如果已经收藏了那就取消收藏
                exist_records.delete()
                return HttpResponse("{'status': 'success', 'msg':'已取消收藏'}", content_type='application/json')
            else:
                ty.favourites += 1
                ty.save()
                user_fav = UserFavourite()
                if int(fav_id) > 0 and int(fav_type):
                    user_fav.fav_type = int(fav_type)
                    user_fav.fav_id = int(fav_id)
                    user_fav.user = request.user
                    user_fav.save()
                    return HttpResponse("{'status': 'success', 'msg':'已收藏'}", content_type='application/json')
                return HttpResponse("{'status': 'fail', 'msg':'收藏出错'}", content_type='application/json')
        # 如果未登录
        return HttpResponse("{'status': 'fail', 'msg':'未登录'}", content_type='application/json')


class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self, request):
        all_teachers = Teacher.objects.all().order_by('-add_time')
        hot_teachers = all_teachers.order_by('-click_nums')[:3]
        # 搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_teachers = Teacher.objects.filter(
                Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword) |
                Q(work_company__icontains=search_keyword) | Q(work_position__icontains=search_keyword))
        teacher_nums = all_teachers.count()
        # 按类别排序
        sort = request.GET.get('sort', '')
        if sort:
            all_teachers = all_teachers.order_by('-click_nums')
        # 用pure_pagination进行分页的核心操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'hot_teachers': hot_teachers,
            'sort': sort,
            'teacher_nums': teacher_nums,
        })


class TeacherDetailView(View):
    '''
    讲师详情页
    '''
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_fav = True
            if UserFavourite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_fav = True
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        all_courses = teacher.course_set.all()
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'hot_teachers': hot_teachers,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav
        })