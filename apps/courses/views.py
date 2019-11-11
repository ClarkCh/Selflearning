from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource
from operation.models import UserFavourite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    '''
    课程总列表页
    '''
    def get(self, request):
        # 对课程机构进行分页并计数和筛选以及按类别排序
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.order_by('-click_nums')[:3]
        # 搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_courses = Course.objects.filter(
                Q(name__icontains=search_keyword)|Q(desc__icontains=search_keyword)|Q(detail__icontains=search_keyword))
        course_nums = all_courses.count()
        # 按类别排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-students')
            else:
                all_courses = all_courses.order_by('-click_nums')
        # 使用pure_pagination进行分页的核心操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'course_nums': course_nums,
            'hot_courses': hot_courses,
            'sort': sort,
        })



class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_type=1, fav_id=course_id):
                has_fav_course = True
            if UserFavourite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:3]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.students += 1
        course.save()
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [t.user.id for t in user_courses]
        course_ids = [t.course.id for t in UserCourse.objects.filter(user_id__in=user_ids)]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        course_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resource': course_resource,
            'relate_courses': relate_courses
        })


class CourseCommentView(LoginRequiredMixin, View):
    '''
    课程评论信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [t.user.id for t in user_courses]
        course_ids = [t.course.id for t in UserCourse.objects.filter(user_id__in=user_ids)]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        comments = CourseComments.objects.filter(course=course)
        course_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resource': course_resource,
            'comments': comments,
            'relate_courses': relate_courses
        })


class AddCommentView(View):
    '''
    用户添加课程评论
    '''
    def post(self, request):
        if request.user.is_authenticated:
            course_id = request.POST.get('course_id', 0)
            comment = request.POST.get('comments', '')
            if int(course_id) > 0 and comment:
                course_comment = CourseComments()
                course = Course.objects.get(id=int(course_id))
                course_comment.course = course
                course_comment.user = request.user
                course_comment.comment = comment
                course_comment.save()
                return HttpResponse("{'status': 'success', 'msg':'添加成功'}", content_type='application/json')
            return HttpResponse("{'status': 'fail', 'msg':'添加失败'}", content_type='application/json')
        return HttpResponse("{'status': 'fail', 'msg':'未登录'}", content_type='application/json')




