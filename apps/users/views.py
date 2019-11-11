import json
from django.shortcuts import render
from django.views import View
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse, render_to_response

from users.models import UserProfile, EmailVerifyRecord, Banner
from .forms import *
from utils.email_send import send_code
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavourite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CustomBackend(ModelBackend):
    '''
    修改登录机制，允许email作为账号登录
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return


class IndexView(View):
    '''
    首页
    '''
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        all_courses = Course.objects.filter(is_banner=False).order_by('-favourites')[:6]
        course_orgs = CourseOrg.objects.all().order_by('-favourites')[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'banner_courses': banner_courses,
            'all_courses': all_courses,
            'course_orgs': course_orgs
        })


class LoginView(View):
    '''
    用户登录
    '''
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        return render(request, 'login.html', {
            'all_banners': all_banners
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                return render(request, 'login.html', {'msg': '用户未激活'})
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        return HttpResponseRedirect(reverse('index'))



class LogoutView(View):
    '''
    用户登出
    '''
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    '''
    用户注册(email注册)
    '''
    def get(self, request):
        register_form = RegisterForm()
        all_banners = Banner.objects.all().order_by('index')
        return render(request, 'register.html', {
            'register_form': register_form,
            'all_banners': all_banners
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '用户已注册', 'register_form': register_form})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # 对新注册用户发送欢迎注册的消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册自学网'
            user_message.save()
            send_code(user_name)
            return render(request, 'login.html')
        return render(request, 'register.html', {
            'register_form': register_form
        })


class ActiveView(View):
    '''
    激活用户
    '''
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        return render(request, 'active_fail.html')


class ForgetView(View):
    '''
    忘记密码
    '''
    def get(self, request):
        forget_form = ForgetForm()
        all_banners = Banner.objects.all().order_by('index')
        return render(request, 'forgetpwd.html', {
            'forget_form': forget_form,
            'all_banners': all_banners
        })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form:
            email = request.POST.get('email', '')
            send_code(email=email, send_type=2)
            return render(request, 'send_success.html')
        return HttpResponseRedirect(reverse('forget'))


class ResetView(View):
    '''
    重置密码
    '''
    def get(self, request, reset_code):
        records = EmailVerifyRecord.objects.filter(code=reset_code)
        if records:
            for record in records:
                email = record.email
                return render(request, 'password_reset.html', {
                    'email': email
                })
        return render(request, 'active_fail.html')


class ModifyView(View):
    '''
    修改用户密码
    '''
    def post(self, request):
        reset_form = ResetForm(request.POST)
        email = request.POST.get('email', '')
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {
                    'msg': '两次密码输入不相同',
                    'email': email
                })
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        return render(request, 'password_reset.html', {
            'email': email
        })


class UserInfoView(LoginRequiredMixin, View):
    '''
    用户个人信息页
    '''
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin, View):
    '''
    在个人中心修改头像
    '''
    def post(self, request):
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        return HttpResponse("{'status': 'fail'}", content_type='application/json')


class UpdatePwdView(View):
    '''
    在个人中心修改密码
    '''
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse("{'status': 'fail'}", content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')



class SendEmailCodeView(LoginRequiredMixin, View):
    '''
    修改邮箱时发送验证码
    '''
    def get(self, request):
        # 为什么这里会是get方法, 因为这里只是点击了申请验证码而已，没有主动发送内容(当然点击申请验证码里面自动包含了email)
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email': '邮箱已经存在'}", content_type='application/json')
        send_code(email=email, send_type=1)
        return HttpResponse("{'status': 'success'}", content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''
    修改邮箱发送验证码后进行验证，使用post方法
    '''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        exist_record = EmailVerifyRecord.objects.filter(email=email, send_type='change', code=code)
        if exist_record:
            request.user.email = email
            request.user.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        return HttpResponse("{'email': '验证码出错'}", content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    '''
    用户中心-我的课程页面
    '''
    def get(self, request):
        all_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'all_courses': all_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    '''
    用户中心-我的收藏中的机构页面
    '''
    def get(self, request):
        orgs = UserFavourite.objects.filter(user=request.user, fav_type=2)
        org_ids = [t.fav_id for t in orgs]
        all_orgs = CourseOrg.objects.filter(id__in=org_ids)
        return render(request, 'usercenter-fav-org.html', {
            'all_orgs': all_orgs,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    '''
    用户中心-我的收藏中的机构页面
    '''
    def get(self, request):
        teachers = UserFavourite.objects.filter(user=request.user, fav_type=3)
        org_ids = [t.fav_id for t in teachers]
        all_teachers = Teacher.objects.filter(id__in=org_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'all_teachers': all_teachers,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    '''
    用户中心-我的收藏中的机构页面
    '''
    def get(self, request):
        courses = UserFavourite.objects.filter(user=request.user, fav_type=1)
        org_ids = [t.fav_id for t in courses]
        all_courses = Course.objects.filter(id__in=org_ids)
        return render(request, 'usercenter-fav-course.html', {
            'all_courses': all_courses,
        })


class MyMessageView(LoginRequiredMixin, View):
    '''
    用户中心-我的消息
    '''
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')
        unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for t in unread_message:
            t.has_read = True
            t.save()
        # 使用pure_pagination进行分页的核心操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 2, request=request)
        message = p.page(page)
        return render(request, 'usercenter-message.html', {
            'all_message': message
        })


def page_not_found(request, exception):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response