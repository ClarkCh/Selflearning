import xadmin
from xadmin import views

from .models import *


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSetting:
    site_title = '自学网后台管理系统'
    site_footer = '在线自学网'
    menu_style = 'accordion'


# class nick_nameAdmin(object):
#     list_display = ['birthday', 'gender', 'address', 'mobile', 'image']
#     search_fields = ['birthday', 'gender', 'address', 'mobile', 'image']
#     list_filter = ['birthday', 'gender', 'address', 'mobile', 'image']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'add_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
