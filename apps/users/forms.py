# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms

from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(min_length=8, required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, required=True)
    captcha = CaptchaField()


class ResetForm(forms.Form):
    password1 = forms.CharField(min_length=8, required=True)
    password2 = forms.CharField(min_length=8, required=True)


class ImageUploadForm(forms.ModelForm):
    '''
    这部分用来修改用户中心的头像
    '''
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    '''
    这部分用来修改用户中心除了头像密码邮箱外的内容
    '''
    def clean_mobile(self):
        return datetime.strptime(self.cleaned_data['birthday'], '%Y-%m-%d').time()

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']