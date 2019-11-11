from django.urls import path

from .views import *


urlpatterns = [
    # 用户个人中心页
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    path('image/upload/', ImageUploadView.as_view(), name='image_upload'),
    # 用户中心修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 用户个人中心修改email
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    # 修改个人资料
    path('update_info/', UserInfoView.as_view(), name='update_info'),
    # 用户中心-我的课程
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    # 用户中心-我收藏的机构
    path('myfav_org/', MyFavOrgView.as_view(), name='myfav_org'),
    # 用户中心-我收藏的教师
    path('myfav_teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 用户中心-我收藏的课程
    path('myfav_course/', MyFavCourseView.as_view(), name='myfav_course'),
    # 用户中心-消息
    path('mymessage/', MyMessageView.as_view(), name='mymessage'),
]
