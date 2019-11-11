import xadmin

from .models import *


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course', 'add_time']
    search_fields = ['name', 'mobile', 'course']
    list_filter = ['name', 'mobile', 'course', 'add_time']


class UserCommentsAdmin(object):
    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']
    list_filter = ['user', 'course', 'comment', 'add_time']


class UserFavouriteAdmin(object):
    list_display = ['user', 'fav_type', 'fav_id', 'add_time']
    search_fields = ['user', 'fav_type', 'fav_id']
    list_filter = ['user', 'fav_type', 'fav_id', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, UserCommentsAdmin)
xadmin.site.register(UserFavourite, UserFavouriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
