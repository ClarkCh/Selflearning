"""Selflearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve
from django.urls import path, include, re_path
from users.views import *
from .settings import MEDIA_ROOT
import xadmin

urlpatterns = [
    # 使用xadmin后台管理
    path('xadmin/', xadmin.site.urls),
    # 验证码功能
    path('captcha/', include('captcha.urls')),
    # 富文本编辑
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # 网站主页
    path('', IndexView.as_view(), name='index'),
    # 登录
    path('login/', LoginView.as_view(), name='login'),
    # 登出
    path('logout/', LogoutView.as_view(), name='logout'),
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    # 激活用户
    path('active/<str:active_code>', ActiveView.as_view(), name='active'),
    # 忘记密码
    path('forget/', ForgetView.as_view(), name='forget'),
    # 忘记密码后重置密码
    path('reset/<str:reset_code>', ResetView.as_view(), name='reset'),
    # 用户中心修改密码
    path('modify/', ModifyView.as_view(), name='modify'),
    # 路由匹配分发
    path('org/', include(('organization.urls', 'org'), namespace='org')),
    path('course/', include(('courses.urls', 'course'), namespace='course')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    # media和static
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # re_path('static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
]


# 全局404, 500页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
