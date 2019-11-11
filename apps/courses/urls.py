from django.urls import path
from .views import *


urlpatterns = [
    # 课程列表展示页
    path('list/', CourseListView.as_view(), name='course_list'),
    # 课程详情展示页
    path('detail/<int:course_id>', CourseDetailView.as_view(), name='course_detail'),
    # 课程具体信息页
    path('info/<int:course_id>', CourseInfoView.as_view(), name='course_info'),
    # 课程评论页
    path('comment/<int:course_id>', CourseCommentView.as_view(), name='course_comment'),
    # 课程评论编辑页
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
]
