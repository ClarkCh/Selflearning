import xadmin

from .models import *


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'city', 'address', 'click_nums', 'favourites', 'image', 'add_time']
    search_fields = ['name', 'desc', 'city', 'address', 'click_nums', 'favourites', 'image']
    list_filter = ['name', 'desc', 'city', 'address', 'click_nums', 'favourites', 'image', 'add_time']
    style_fields = {'desc': 'ueditor'}


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'desc', 'click_nums', 'favourites', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'desc', 'click_nums', 'favourites']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'desc', 'click_nums', 'favourites', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
