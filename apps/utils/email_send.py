from users.models import EmailVerifyRecord
from random import randint

from django.core.mail import send_mail
from Selflearning.settings import EMAIL_FROM


def send_code(email, send_type=0):
    '''
    发送邮箱验证码，0为注册1为修改邮箱2为找回密码
    '''
    email_record = EmailVerifyRecord()
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if send_type == 0:
        size = 12
        email_record.send_type = 'register'
        email_title = '自学网注册激活链接'
        before_content = '请点击如下链接以激活您的账号, '
    else:
        size = 4
        if send_type == 1:
            email_record.send_type = 'change'
            email_title = '自学网修改邮箱链接'
            before_content = '请点击如下链接以修改您的账号邮箱, '
        else:
            email_record.send_type = 'forget'
            email_title = '自学网重置密码链接'
            before_content = '请点击如下链接以重置您的密码, '
    lst = []
    for t in range(size):
        lst.append(string[randint(0, 61)])
    code = ''.join(lst)
    email_record.code = code
    email_record.email = email
    email_record.save()
    email_content = before_content + 'http://127.0.0.1:8000/reset/%s' % (code)
    send_mail(email_title, email_content, EMAIL_FROM, [email])



