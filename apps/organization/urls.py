from django.urls import path
from .views import *


urlpatterns = [
    # 机构列表页
    path('list/', OrgView.as_view(), name='org_list'),
    # 增加'我要学习'的功能
    path('add_ask/', AddAskView.as_view(), name='add_ask'),
    # 机构的主页
    path('home/<int:org_id>', OrgHomeView.as_view(), name='org_home'),
    # 机构下的课程页
    path('course/<int:org_id>', OrgCourseView.as_view(), name='org_course'),
    # 机构的详情描述页
    path('desc/<int:org_id>', OrgDescView.as_view(), name='org_desc'),
    # 机构的讲师页
    path('org_teacher/<int:org_id>', OrgTeacherView.as_view(), name='org_teacher'),
    # 收藏功能(包括课程、机构、讲师, 用整型类型和id来确定, 而不是外键)
    path('add_fav/', AddFavView.as_view(), name='add_fav'),
    # 讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    # 讲师的详解介绍页
    path('teacher_detail/<int:teacher_id>', TeacherDetailView.as_view(), name='teacher_detail'),
]
